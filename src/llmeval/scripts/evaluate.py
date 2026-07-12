# %% IMPORTS -----
import logging
import math
import subprocess
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from importlib.metadata import version
from typing import cast

import logfire
from pydantic_evals import (
    Case,
    Dataset,
    increment_eval_metric,
    set_eval_attribute,
)
from pydantic_evals.evaluators import (
    EvaluationReason,
    Evaluator,
    EvaluatorContext,
)
from ragas.metrics.collections import (
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
)
from ragas.metrics.result import MetricResult

from llmeval.utils.config import (
    CASES_PATH,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    EVAL_MAX_CONCURRENCY,
    INDEX_VERSION,
    MODEL_MAX_TOKENS,
    MODEL_NAME,
    MODEL_TEMPERATURE,
    PROMPT_VERSION,
    RAGAS_ANSWER_RELEVANCY_STRICTNESS,
    RETRIEVAL_STRATEGY,
    SEARCH_K,
)
from llmeval.utils.eval_schemas import (
    EvalCasesFile,
    RagAnswer,
    RagAnswerVisible,
    RagEvalInput,
    RagEvalMetadata,
    RagExpectedOutput,
    RetrievalStats,
    RetrievedContext,
    load_eval_cases,
)
from llmeval.utils.logfire_datasets import (
    HostedRagDataset,
    push_and_fetch_hosted_dataset,
)
from llmeval.utils.observability import configure_logfire
from llmeval.utils.rag_agent import (
    MistralRagasEmbeddings,
    MistralRagasLLM,
    MistralCallStats,
    RagAgent,
)
from llmeval.utils.reports import write_reports
from llmeval.utils.vector_store import VectorStoreManager

RagEvalOutput = RagExpectedOutput | RagAnswerVisible | str
RuntimeRagDataset = Dataset[RagEvalInput, RagEvalOutput, RagEvalMetadata]


@dataclass
class RagasMetricRun:
    result: MetricResult
    seconds: float
    stats: MistralCallStats


# %% RAGAS EVALUATOR -----
@dataclass(repr=False)
class RagasEvaluator(Evaluator[RagEvalInput, RagEvalOutput, RagEvalMetadata]):
    model_name: str = MODEL_NAME
    embedding_model: str = EMBEDDING_MODEL
    answer_relevancy_strictness: int = RAGAS_ANSWER_RELEVANCY_STRICTNESS

    def __post_init__(self) -> None:
        self._llm = MistralRagasLLM(model_name=self.model_name)
        self._embeddings = MistralRagasEmbeddings(model_name=self.embedding_model)

        self._faithfulness = Faithfulness(llm=self._llm)
        self._answer_relevancy = AnswerRelevancy(
            llm=self._llm,
            embeddings=self._embeddings,
            strictness=self.answer_relevancy_strictness,
        )
        self._context_precision = ContextPrecision(llm=self._llm)
        self._context_recall = ContextRecall(llm=self._llm)

    async def evaluate(
        self,
        ctx: EvaluatorContext[RagEvalInput, RagEvalOutput, RagEvalMetadata],
    ) -> dict[str, EvaluationReason]:
        if not isinstance(ctx.output, RagAnswerVisible):
            raise TypeError("RagasEvaluator expects a RagAnswerVisible task output.")
        if not isinstance(ctx.expected_output, RagExpectedOutput):
            raise TypeError("RagasEvaluator expects a RagExpectedOutput reference.")
        full_answer = ctx.output.full_answer
        if full_answer is None:
            raise ValueError("RAGAS evaluation requires the full internal answer.")

        contexts = [context.text for context in full_answer.contexts]
        if not contexts:
            raise ValueError("At least one retrieved context is required by RAGAS.")

        ragas_started = time.perf_counter()
        with logfire.span(
            "evaluate_ragas_metrics id_question={id_question}",
            id_question=ctx.inputs.id_question,
            metric_count=4,
            judge_model=self.model_name,
            embedding_model=self.embedding_model,
        ):
            faithfulness = await self._score_metric(
                "faithfulness",
                self._faithfulness.ascore,
                user_input=ctx.inputs.question,
                response=full_answer.answer,
                retrieved_contexts=contexts,
            )
            answer_relevancy = await self._score_metric(
                "answer_relevancy",
                self._answer_relevancy.ascore,
                user_input=ctx.inputs.question,
                response=full_answer.answer,
            )
            context_precision = await self._score_metric(
                "context_precision",
                self._context_precision.ascore,
                user_input=ctx.inputs.question,
                reference=ctx.expected_output.answer,
                retrieved_contexts=contexts,
            )
            context_recall = await self._score_metric(
                "context_recall",
                self._context_recall.ascore,
                user_input=ctx.inputs.question,
                retrieved_contexts=contexts,
                reference=ctx.expected_output.answer,
            )
        ragas_total_seconds = time.perf_counter() - ragas_started

        metric_runs = {
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy,
            "context_precision": context_precision,
            "context_recall": context_recall,
        }
        _record_ragas_metrics(ctx, metric_runs, ragas_total_seconds)

        return {
            "faithfulness": _to_evaluation_reason(faithfulness.result),
            "answer_relevancy": _to_evaluation_reason(answer_relevancy.result),
            "context_precision": _to_evaluation_reason(context_precision.result),
            "context_recall": _to_evaluation_reason(context_recall.result),
        }

    def get_evaluator_version(self) -> str:
        return version("ragas")

    async def _score_metric(
        self,
        name: str,
        scorer: Callable[..., Awaitable[object]],
        **kwargs: object,
    ) -> RagasMetricRun:
        llm_before = self._llm.stats_snapshot()
        embeddings_before = self._embeddings.stats_snapshot()
        started_at = time.perf_counter()

        with logfire.span("ragas_metric metric={metric}", metric=name):
            result = await scorer(**kwargs)

        seconds = time.perf_counter() - started_at
        llm_delta = self._llm.stats_snapshot().delta(llm_before)
        embeddings_delta = self._embeddings.stats_snapshot().delta(embeddings_before)
        stats = MistralCallStats(
            wait_seconds=llm_delta.wait_seconds + embeddings_delta.wait_seconds,
            api_seconds=llm_delta.api_seconds + embeddings_delta.api_seconds,
            request_count=llm_delta.request_count,
            input_tokens=llm_delta.input_tokens,
            output_tokens=llm_delta.output_tokens,
            total_tokens=llm_delta.total_tokens,
            embedding_request_count=embeddings_delta.embedding_request_count,
        )
        metric_result = cast(MetricResult, result)
        _record_ragas_metric_span(
            name=name,
            result=metric_result,
            seconds=seconds,
            stats=stats,
        )

        return RagasMetricRun(
            result=metric_result,
            seconds=seconds,
            stats=stats,
        )


def _to_evaluation_reason(result: MetricResult) -> EvaluationReason:
    score = float(result.value)
    if not math.isfinite(score):
        raise ValueError("RAGAS returned a non-finite score.")

    return EvaluationReason(
        value=score,
        reason=result.reason,
    )


def _record_ragas_metrics(
    ctx: EvaluatorContext[RagEvalInput, RagEvalOutput, RagEvalMetadata],
    metric_runs: dict[str, RagasMetricRun],
    total_seconds: float,
) -> None:
    total_stats = MistralCallStats()

    ctx.metrics["ragas_total_seconds"] = total_seconds
    for metric_name, metric_run in metric_runs.items():
        stats = metric_run.stats
        total_stats.wait_seconds += stats.wait_seconds
        total_stats.api_seconds += stats.api_seconds
        total_stats.request_count += stats.request_count
        total_stats.input_tokens += stats.input_tokens
        total_stats.output_tokens += stats.output_tokens
        total_stats.total_tokens += stats.total_tokens
        total_stats.embedding_request_count += stats.embedding_request_count

        prefix = _ragas_metric_prefix(metric_name)
        ctx.metrics[f"{prefix}_seconds"] = metric_run.seconds
        ctx.metrics[f"{prefix}_score"] = float(metric_run.result.value)
        ctx.metrics[f"{prefix}_wait_seconds"] = stats.wait_seconds
        ctx.metrics[f"{prefix}_api_seconds"] = stats.api_seconds
        ctx.metrics[f"{prefix}_request_count"] = stats.request_count
        ctx.metrics[f"{prefix}_input_tokens"] = stats.input_tokens
        ctx.metrics[f"{prefix}_output_tokens"] = stats.output_tokens
        ctx.metrics[f"{prefix}_total_tokens"] = stats.total_tokens

    ctx.metrics["ragas_wait_seconds"] = total_stats.wait_seconds
    ctx.metrics["ragas_api_seconds"] = total_stats.api_seconds
    ctx.metrics["judge_request_count"] = total_stats.request_count
    ctx.metrics["judge_input_tokens"] = total_stats.input_tokens
    ctx.metrics["judge_output_tokens"] = total_stats.output_tokens
    ctx.metrics["judge_total_tokens"] = total_stats.total_tokens
    ctx.metrics["embedding_request_count"] = total_stats.embedding_request_count


def _record_ragas_metric_span(
    name: str,
    result: MetricResult,
    seconds: float,
    stats: MistralCallStats,
) -> None:
    with logfire.span(
        "ragas_metric_values metric={metric}",
        metric=name,
        score=float(result.value),
        seconds=seconds,
        wait_seconds=stats.wait_seconds,
        api_seconds=stats.api_seconds,
        request_count=stats.request_count,
        input_tokens=stats.input_tokens,
        output_tokens=stats.output_tokens,
        total_tokens=stats.total_tokens,
        embedding_request_count=stats.embedding_request_count,
    ):
        pass


def _ragas_metric_prefix(metric_name: str) -> str:
    return {
        "faithfulness": "faithfulness",
        "answer_relevancy": "relevancy",
        "context_precision": "precision",
        "context_recall": "recall",
    }[metric_name]


# %% PYDANTIC EVALS DATASET -----
def build_hosted_eval_dataset(
    eval_file: EvalCasesFile,
) -> HostedRagDataset:
    cases = [
        Case[
            RagEvalInput,
            RagExpectedOutput,
            RagEvalMetadata,
        ](
            name=case.id,
            inputs=RagEvalInput(
                id_question=case.id,
                question=case.question,
            ),
            expected_output=RagExpectedOutput.from_eval_case(case),
            metadata=RagEvalMetadata(
                category=case.category,
                source_type=case.source_type,
                language=case.language,
                evidence_notes=case.evidence_notes,
            ),
        )
        for case in eval_file.cases
    ]

    return Dataset[
        RagEvalInput,
        RagExpectedOutput,
        RagEvalMetadata,
    ](
        name=eval_file.metadata.dataset_name,
        cases=cases,
    )


def with_ragas_evaluator(dataset: HostedRagDataset) -> RuntimeRagDataset:
    return Dataset[
        RagEvalInput,
        RagEvalOutput,
        RagEvalMetadata,
    ](
        name=dataset.name,
        cases=cast(
            "list[Case[RagEvalInput, RagEvalOutput, RagEvalMetadata]]",
            dataset.cases,
        ),
        evaluators=[RagasEvaluator()],
    )


def build_eval_dataset(eval_file: EvalCasesFile) -> RuntimeRagDataset:
    return with_ragas_evaluator(build_hosted_eval_dataset(eval_file))


# %% EVALUATION TASK -----
def build_rag_task(
    vector_store: VectorStoreManager,
    rag_agent: RagAgent,
    run_attributes: dict[str, object],
):
    def run_rag(inputs: RagEvalInput) -> RagAnswerVisible:
        # !! Retrieve contexts -----
        with logfire.span(
            "search_contexts id_question={id_question}",
            id_question=inputs.id_question,
            search_k=SEARCH_K,
        ):
            retrieval_started = time.perf_counter()
            search_results = vector_store.search(inputs.question, k=SEARCH_K)
            retrieval_seconds = time.perf_counter() - retrieval_started
            contexts = [
                RetrievedContext.from_search_result(item) for item in search_results
            ]
            retrieval_stats = _retrieval_stats(contexts, retrieval_seconds)

        # !! Generate answer -----
        full_answer = rag_agent.answer(
            case_id=inputs.id_question,
            question=inputs.question,
            contexts=contexts,
        )
        full_answer.retrieval = retrieval_stats

        # !! Expose task data to Pydantic Evals and Logfire -----
        for name, value in run_attributes.items():
            set_eval_attribute(name, value)

        set_eval_attribute(
            "retrieved_sources",
            list(dict.fromkeys(context.source for context in contexts)),
        )
        set_eval_attribute("used_sources", full_answer.used_sources)
        set_eval_attribute("insufficient_context", full_answer.insufficient_context)
        set_eval_attribute("confidence", full_answer.confidence)
        _record_product_metrics(full_answer)
        _record_product_metrics_span(
            inputs=inputs,
            answer=full_answer,
            run_attributes=run_attributes,
        )

        return full_answer.to_visible()

    return run_rag


def _retrieval_stats(
    contexts: list[RetrievedContext],
    seconds: float,
) -> RetrievalStats:
    scores = [context.score for context in contexts]
    sources = list(dict.fromkeys(context.source for context in contexts))

    return RetrievalStats(
        seconds=seconds,
        context_count=len(contexts),
        top_score=max(scores) if scores else None,
        mean_score=sum(scores) / len(scores) if scores else None,
        total_chars=sum(len(context.text) for context in contexts),
        source_count=len(sources),
    )


def _record_product_metrics(answer: RagAnswer) -> None:
    retrieval = answer.retrieval
    generation = answer.generation
    task_seconds = retrieval.seconds + generation.seconds

    _increment_metric("retrieval_seconds", retrieval.seconds)
    _increment_metric("retrieval_context_count", retrieval.context_count)
    _increment_optional_metric("retrieval_top_score", retrieval.top_score)
    _increment_optional_metric("retrieval_mean_score", retrieval.mean_score)
    _increment_metric("retrieval_total_chars", retrieval.total_chars)
    _increment_metric("retrieved_source_count", retrieval.source_count)
    _increment_metric("generation_seconds", generation.seconds)
    _increment_metric("answer_input_tokens", generation.input_tokens)
    _increment_metric("answer_output_tokens", generation.output_tokens)
    _increment_metric("answer_total_tokens", generation.total_tokens)
    _increment_metric("answer_request_count", generation.request_count)
    _increment_metric("answer_chars", generation.answer_chars)
    _increment_metric("task_seconds", task_seconds)


def _record_product_metrics_span(
    inputs: RagEvalInput,
    answer: RagAnswer,
    run_attributes: dict[str, object],
) -> None:
    retrieval = answer.retrieval
    generation = answer.generation

    with logfire.span(
        "rag_product_metrics id_question={id_question}",
        id_question=inputs.id_question,
        retrieval_strategy=run_attributes.get("retrieval_strategy"),
        search_k=run_attributes.get("search_k"),
        answer_model=run_attributes.get("answer_model"),
        prompt_version=run_attributes.get("prompt_version"),
        retrieval_seconds=retrieval.seconds,
        retrieval_context_count=retrieval.context_count,
        retrieval_top_score=retrieval.top_score,
        retrieval_mean_score=retrieval.mean_score,
        retrieval_total_chars=retrieval.total_chars,
        retrieved_source_count=retrieval.source_count,
        generation_seconds=generation.seconds,
        answer_input_tokens=generation.input_tokens,
        answer_output_tokens=generation.output_tokens,
        answer_total_tokens=generation.total_tokens,
        answer_request_count=generation.request_count,
        answer_chars=generation.answer_chars,
        task_seconds=retrieval.seconds + generation.seconds,
        confidence=answer.confidence,
        insufficient_context=answer.insufficient_context,
    ):
        pass


def _increment_metric(name: str, value: int | float) -> None:
    increment_eval_metric(name, value)


def _increment_optional_metric(name: str, value: int | float | None) -> None:
    if value is not None:
        increment_eval_metric(name, value)


def build_run_metadata(eval_file: EvalCasesFile) -> dict[str, object]:
    return {
        "dataset_version": eval_file.metadata.version,
        "experiment_name": eval_file.metadata.experiment_name,
        "git_commit": _git_commit(),
        "prompt_version": PROMPT_VERSION,
        "answer_model": MODEL_NAME,
        "judge_model": MODEL_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "retrieval_strategy": RETRIEVAL_STRATEGY,
        "search_k": SEARCH_K,
        "index_version": INDEX_VERSION,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "temperature": MODEL_TEMPERATURE,
        "max_tokens": MODEL_MAX_TOKENS,
        "ragas_version": version("ragas"),
        "pydantic_evals_version": version("pydantic-evals"),
    }


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"

    return result.stdout.strip() or "unknown"


# %% EVALUATION PIPELINE -----
def main() -> None:
    started_at = time.perf_counter()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    configure_logfire()

    # !! Load evaluation cases -----
    with logfire.span("load_eval_cases path={path}", path=str(CASES_PATH)):
        eval_file = load_eval_cases(CASES_PATH)

    logging.info(
        "Loaded %s cases from dataset %s v%s",
        len(eval_file.cases),
        eval_file.metadata.dataset_name,
        eval_file.metadata.version,
    )

    # !! Initialize the task and dataset -----
    with logfire.span("initialize_rag_evaluation"):
        run_metadata = build_run_metadata(eval_file)
        local_dataset = build_hosted_eval_dataset(eval_file)
        hosted_dataset = push_and_fetch_hosted_dataset(
            dataset=local_dataset,
            eval_file=eval_file,
        )
        dataset = with_ragas_evaluator(hosted_dataset)
        vector_store = VectorStoreManager()
        rag_agent = RagAgent()
        rag_task = build_rag_task(vector_store, rag_agent, run_metadata)

    logging.info(
        "Synced hosted Logfire dataset %s with %s cases",
        dataset.name,
        len(dataset.cases),
    )

    # !! Run the Pydantic Evals experiment -----
    report = dataset.evaluate_sync(
        rag_task,
        name=eval_file.metadata.experiment_name,
        task_name="nba_rag",
        max_concurrency=EVAL_MAX_CONCURRENCY,
        metadata=run_metadata,
    )

    report.print(include_reasons=True)

    execution_seconds = time.perf_counter() - started_at

    with logfire.span(
        "write_reports dataset_version={dataset_version}",
        dataset_name=eval_file.metadata.dataset_name,
        dataset_version=eval_file.metadata.version,
        experiment_name=eval_file.metadata.experiment_name,
        execution_seconds=execution_seconds,
    ):
        details_csv, report_md = write_reports(
            eval_file=eval_file,
            report=report,
            execution_seconds=execution_seconds,
        )

    logging.info("Wrote %s", details_csv)
    logging.info("Wrote %s", report_md)

    evaluator_failure_count = sum(len(case.evaluator_failures) for case in report.cases)
    if report.failures or evaluator_failure_count:
        raise RuntimeError(
            "Evaluation completed with "
            f"{len(report.failures)} task failure(s) and "
            f"{evaluator_failure_count} evaluator failure(s)."
        )


if __name__ == "__main__":
    main()
