import asyncio
from typing import Any

import logfire
from langchain_core.outputs import Generation, LLMResult
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from ragas.embeddings import BaseRagasEmbeddings
from ragas.llms import BaseRagasLLM

from .config import EMBEDDING_MODEL, MISTRAL_API_KEY, MODEL_NAME
from .eval_schemas import RagAnswer, RetrievedContext

SYSTEM_PROMPT = """Tu es 'NBA Analyst AI', un assistant expert sur la ligue de basketball NBA.
Ta mission est de répondre aux questions des fans en animant le débat.

Réponds en français. Base-toi uniquement sur le contexte fourni.
Si les informations disponibles ne permettent pas de répondre précisément,
dis-le clairement au lieu d'inventer un chiffre ou un fait.

---
{context_str}
---

QUESTION DU FAN:
{question}

RÉPONSE DE L'ANALYSTE NBA:"""


class RagAgent:
    def __init__(self, model_name: str = MODEL_NAME):
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required to run the evaluation.")
        self.model_name = model_name
        self.client = MistralClient(api_key=MISTRAL_API_KEY)

    def answer(self, question: str, contexts: list[RetrievedContext]) -> RagAnswer:
        context_str = self._format_contexts(contexts)
        prompt = SYSTEM_PROMPT.format(context_str=context_str, question=question)

        with logfire.span(
            "llm_answer question={question}",
            question=question,
            model=self.model_name,
            context_count=len(contexts),
        ):
            response = self.client.chat(
                model=self.model_name,
                messages=[ChatMessage(role="user", content=prompt)],
                temperature=0.1,
            )

        if not response.choices:
            answer = "Je n'ai pas pu générer de réponse."
        else:
            answer = response.choices[0].message.content

        raw_answer = RagAnswer(
            question=question,
            answer=answer,
            contexts=contexts,
            model=self.model_name,
        )
        return validate_with_pydantic_ai(raw_answer)

    @staticmethod
    def _format_contexts(contexts: list[RetrievedContext]) -> str:
        if not contexts:
            return (
                "Aucune information pertinente trouvée dans la base de connaissances."
            )

        return "\n\n---\n\n".join(
            f"Source: {ctx.source} (Score: {ctx.score:.1f}%)\nContenu: {ctx.text}"
            for ctx in contexts
        )


def validate_with_pydantic_ai(answer: RagAnswer) -> RagAnswer:
    """Use Pydantic AI in a minimal local mode to validate the structured output."""
    agent = Agent(
        TestModel(custom_output_args=answer.model_dump()),
        output_type=RagAnswer,
        system_prompt="Valide la structure de cette réponse RAG.",
    )
    result = agent.run_sync("Valide et retourne l'objet fourni.")
    return result.output


class MistralRagasLLM(BaseRagasLLM):
    def __init__(self, model_name: str = MODEL_NAME):
        super().__init__()
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required for RAGAS LLM judging.")
        self.model_name = model_name
        self.client = MistralClient(api_key=MISTRAL_API_KEY)

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
            response = self.client.chat(
                model=self.model_name,
                messages=[ChatMessage(role="user", content=prompt_text)],
                temperature=temperature,
            )
            text = response.choices[0].message.content if response.choices else ""
            generations.append(
                Generation(text=text, generation_info={"finish_reason": "stop"})
            )

        return LLMResult(
            generations=[generations], llm_output={"model": self.model_name}
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


class MistralRagasEmbeddings(BaseRagasEmbeddings):
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        super().__init__()
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is required for RAGAS embeddings.")
        self.model_name = model_name
        self.client = MistralClient(api_key=MISTRAL_API_KEY)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings(model=self.model_name, input=texts)
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self.embed_documents, texts)

    async def aembed_query(self, text: str) -> list[float]:
        return await asyncio.to_thread(self.embed_query, text)
