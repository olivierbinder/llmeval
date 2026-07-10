# %% IMPORTS -----
import asyncio
import threading
import time
from typing import Any, Literal

import logfire
from langchain_core.outputs import Generation, LLMResult
from mistralai.client import Mistral
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from ragas.embeddings import BaseRagasEmbeddings
from ragas.llms import BaseRagasLLM

from .config import EMBEDDING_MODEL, MISTRAL_API_KEY, MODEL_NAME
from .eval_schemas import RagAnswer, RetrievedContext

# %% PROMPTS -----
SYSTEM_PROMPT = """Tu es NBA Analyst AI, un assistant spécialisé sur la NBA.

Règles obligatoires :
- Réponds en français.
- Base-toi uniquement sur les contextes fournis.
- Réponds de façon concise : maximum 5 phrases.
- N'utilise pas de titres, de listes, de markdown complexe ou d'emojis.
- Ne cite pas de noms d'utilisateurs Reddit.
- N'ajoute aucune source externe.
- Si les contextes ne permettent pas de répondre précisément, dis-le clairement.
- Pour une question quantitative, n'invente jamais de chiffre absent des contextes.
- Les sources utilisées doivent être choisies uniquement parmi les sources présentes dans les contextes.
"""

USER_PROMPT = """CONTEXTES DISPONIBLES :
{context_str}

QUESTION :
{question}
"""


# %% RATE LIMITER -----
class MistralRateLimiter:
    def __init__(self, min_interval_seconds: float):
        self.min_interval_seconds = min_interval_seconds
        self._lock = threading.Lock()
        self._last_call_at = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_call_at
            remaining = self.min_interval_seconds - elapsed

            if remaining > 0:
                time.sleep(remaining)

            self._last_call_at = time.monotonic()


MISTRAL_RAGAS_RATE_LIMITER = MistralRateLimiter(
    min_interval_seconds=4.0,
)


# %% STRUCTURED OUTPUT -----
class StructuredRagOutput(BaseModel):
    answer: str = Field(
        max_length=700,
        description=(
            "Réponse finale en français, concise, sans markdown complexe, "
            "sans emoji et sans source externe."
        ),
    )
    used_sources: list[str] = Field(
        default_factory=list,
        max_length=3,
        description="Sources réellement utilisées pour construire la réponse.",
    )
    insufficient_context: bool = Field(
        description=(
            "True si les contextes ne permettent pas de répondre précisément."
        ),
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description="Niveau de confiance basé uniquement sur les contextes fournis."
    )

    # Answer constraints
    @field_validator("answer")
    @classmethod
    def answer_must_be_plain_text(cls, value: str) -> str:
        value = value.strip()

        forbidden_tokens = ["###", "**", "```", "🏀", "🔥"]
        if any(token in value for token in forbidden_tokens):
            raise ValueError(
                "La réponse doit être du texte simple, sans markdown, liste ou emoji."
            )

        sentence_count = sum(value.count(mark) for mark in [".", "?", "!"])
        if sentence_count > 5:
            raise ValueError("La réponse doit faire maximum 5 phrases.")

        return value

    @field_validator("answer")
    @classmethod
    def answer_must_not_look_truncated(cls, value: str) -> str:
        value = value.strip()

        bad_endings = ("(", "[", "{", ",", ";", ":", " et", " ou", " mais", " car")
        if value.endswith(bad_endings):
            raise ValueError("La réponse semble tronquée.")

        return value

    # Source constraints
    @field_validator("used_sources")
    @classmethod
    def used_sources_must_be_clean(cls, value: list[str]) -> list[str]:
        cleaned_sources = [source.strip() for source in value if source.strip()]
        return list(dict.fromkeys(cleaned_sources))


# %% RAG AGENT WITH PYDANTIC AI -----
class RagAgent:
    def __init__(self, model_name: str = MODEL_NAME):
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required to run the evaluation.")

        self.model_name = model_name

        model = MistralModel(  # Modèle utilisé par Pydantic IA
            self.model_name,
            provider=MistralProvider(api_key=MISTRAL_API_KEY),
        )

        self.agent = Agent(  # Agent Pydantic IA
            model,
            output_type=StructuredRagOutput,  # Contraintes sur l'output
            system_prompt=SYSTEM_PROMPT,
            model_settings=ModelSettings(  # Contraintes sur le model
                temperature=0.1,
                max_tokens=1200,
            ),
        )

    def answer(self, question: str, contexts: list[RetrievedContext]) -> RagAnswer:
        context_str = self._format_contexts(contexts)
        prompt = USER_PROMPT.format(context_str=context_str, question=question)

        with logfire.span(
            "llm_answer question={question}",
            question=question,
            model=self.model_name,
            context_count=len(contexts),
            structured_output=True,
        ):
            result = self.agent.run_sync(prompt)

        structured_answer = self._normalize_structured_answer(
            output=result.output,
            contexts=contexts,
        )

        return RagAnswer(
            question=question,
            answer=structured_answer.answer,
            contexts=contexts,
            model=self.model_name,
            used_sources=structured_answer.used_sources,
            insufficient_context=structured_answer.insufficient_context,
            confidence=structured_answer.confidence,
        )

    @staticmethod
    def _format_contexts(contexts: list[RetrievedContext]) -> str:
        if not contexts:
            return (
                "Aucune information pertinente trouvée dans la base de connaissances."
            )

        return "\n\n---\n\n".join(
            f"Source: {ctx.source} (Score: {ctx.score:.1f})\nContenu: {ctx.text}"
            for ctx in contexts
        )

    @staticmethod
    def _normalize_structured_answer(
        output: StructuredRagOutput,
        contexts: list[RetrievedContext],
    ) -> StructuredRagOutput:
        available_sources = list(dict.fromkeys(ctx.source for ctx in contexts))

        used_sources = [
            source for source in output.used_sources if source in available_sources
        ]

        if not used_sources and not output.insufficient_context:
            used_sources = available_sources[:1]

        return StructuredRagOutput(
            answer=output.answer,
            used_sources=used_sources,
            insufficient_context=output.insufficient_context,
            confidence=output.confidence,
        )


# %% RAGAS LLM TO SCORE ANSWERS -----
class MistralRagasLLM(BaseRagasLLM):
    def __init__(self, model_name: str = MODEL_NAME):
        super().__init__()

        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required for RAGAS LLM judging.")

        self.model_name = model_name
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def generate_text(
        self,
        prompt: Any,
        n: int = 1,
        temperature: float = 0.01,
        stop: list[str] | None = None,
        callbacks: Any = None,
    ) -> LLMResult:
        prompt_text = (
            prompt.to_string() if hasattr(prompt, "to_string") else str(prompt)
        )
        generations = []

        for _ in range(n):
            request_kwargs: dict[str, Any] = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt_text}],
                "temperature": temperature,
                "stream": False,
            }

            if stop:
                request_kwargs["stop"] = stop

            MISTRAL_RAGAS_RATE_LIMITER.wait()
            response = self.client.chat.complete(**request_kwargs)

            text = ""
            if response.choices:
                content = response.choices[0].message.content
                text = content if isinstance(content, str) else str(content or "")

            generations.append(
                Generation(text=text, generation_info={"finish_reason": "stop"})
            )

        return LLMResult(
            generations=[generations],
            llm_output={"model": self.model_name},
        )

    async def agenerate_text(
        self,
        prompt: Any,
        n: int = 1,
        temperature: float | None = 0.01,
        stop: list[str] | None = None,
        callbacks: Any = None,
    ) -> LLMResult:
        return await asyncio.to_thread(
            self.generate_text,
            prompt,
            n,
            0.01 if temperature is None else temperature,
            stop,
            callbacks,
        )

    def is_finished(self, response: LLMResult) -> bool:
        return True


# %% RAGAS EMBEDER -----
class MistralRagasEmbeddings(BaseRagasEmbeddings):
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        super().__init__()

        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required for RAGAS embeddings.")

        self.model_name = model_name
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        MISTRAL_RAGAS_RATE_LIMITER.wait()
        response = self.client.embeddings.create(
            model=self.model_name,
            inputs=texts,
        )

        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self.embed_documents, texts)

    async def aembed_query(self, text: str) -> list[float]:
        return await asyncio.to_thread(self.embed_query, text)
