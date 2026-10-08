# %% IMPORTS -----
import time
from typing import Literal, cast

import logfire
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from llmeval.utils.config import (
    MISTRAL_API_KEY,
    MODEL_MAX_TOKENS,
    MODEL_NAME,
    MODEL_TEMPERATURE,
)
from llmeval.utils.eval_schemas import GenerationStats, RagAnswer, RetrievedContext


# %% PROMPTS -----
SYSTEM_PROMPT = """Tu es NBA Analyst AI, un assistant spécialisé sur la NBA.

Règles obligatoires :
- Réponds en français.
- Base-toi uniquement sur les contextes fournis.
- Réponds de façon concise : maximum 2 phrases et maximum 40 mots total.
- N'utilise pas de titres, de listes, de markdown complexe ou d'emojis.
- Ne cite pas de noms d'utilisateurs Reddit.
- N'ajoute aucune source externe.
- Identifie précisément l'équipe, le joueur, la métrique ou la période demandée.
- Ignore les passages des contextes qui parlent d'une autre équipe, d'un autre joueur, d'une autre métrique ou d'une autre période.
- Ne mélange jamais deux sujets proches trouvés dans les mêmes contextes.
- Si les contextes pertinents contiennent des avis contradictoires, synthétise seulement les points directement liés à la question.
- Si les contextes ne permettent pas de répondre précisément, dis-le clairement.
- Pour une question quantitative, n'invente jamais de chiffre absent des contextes.
- Les sources utilisées doivent être choisies uniquement parmi les sources présentes dans les contextes.
"""

USER_PROMPT = """CONTEXTES DISPONIBLES :
{context_str}

QUESTION :
{question}
"""


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

        model = MistralModel(
            self.model_name,
            provider=MistralProvider(api_key=MISTRAL_API_KEY),
        )

        self.agent = Agent(
            model,
            output_type=StructuredRagOutput,
            system_prompt=SYSTEM_PROMPT,
            model_settings=ModelSettings(
                temperature=MODEL_TEMPERATURE,
                max_tokens=MODEL_MAX_TOKENS,
            ),
        )

    def answer(
        self,
        case_id: str,
        question: str,
        contexts: list[RetrievedContext],
    ) -> RagAnswer:
        context_str = self._format_contexts(contexts)
        prompt = USER_PROMPT.format(context_str=context_str, question=question)

        with logfire.span(
            "rag_agent_answer case_id={case_id}",
            case_id=case_id,
            question=question,
            model=self.model_name,
            context_count=len(contexts),
            structured_output=True,
        ):
            generation_started = time.perf_counter()
            result = self.agent.run_sync(prompt)
            generation_seconds = time.perf_counter() - generation_started

        structured_output = cast(StructuredRagOutput, result.output)
        structured_answer = self._normalize_structured_answer(
            output=structured_output,
            contexts=contexts,
        )
        generation_stats = _generation_stats_from_result(
            result=result,
            seconds=generation_seconds,
            answer=structured_answer.answer,
        )

        return RagAnswer(
            question=question,
            answer=structured_answer.answer,
            contexts=contexts,
            model=self.model_name,
            used_sources=structured_answer.used_sources,
            insufficient_context=structured_answer.insufficient_context,
            confidence=structured_answer.confidence,
            generation=generation_stats,
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


def _generation_stats_from_result(
    result: object,
    seconds: float,
    answer: str,
) -> GenerationStats:
    usage = getattr(result, "usage", None)
    input_tokens = _int_attr(usage, "input_tokens")
    output_tokens = _int_attr(usage, "output_tokens")

    return GenerationStats(
        seconds=seconds,
        api_seconds=seconds,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        request_count=_int_attr(usage, "requests"),
        answer_chars=len(answer),
    )


def _int_attr(obj: object, name: str) -> int:
    value = getattr(obj, name, 0)
    return int(value or 0)
