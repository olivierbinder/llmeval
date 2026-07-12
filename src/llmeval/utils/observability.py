# %% IMPORTS -----
import logging

import logfire
from logfire import ConsoleOptions


# %% LOGFIRE CONFIGURATION -----
def configure_logfire() -> None:
    """Configure Logfire for local console and Logfire web UI."""
    try:
        logfire.configure(
            service_name="nba-rag-evaluation",
            console=ConsoleOptions(span_style="simple"),
            inspect_arguments=False,
            metrics=logfire.MetricsOptions(collect_in_spans=True),
        )
        logfire.instrument_pydantic(record="failure")
        logfire.instrument_pydantic_ai()
        logfire.instrument_system_metrics()
    except Exception as exc:
        logging.warning("Logfire could not be configured: %s", exc)
