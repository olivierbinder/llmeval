import logging

import logfire


def configure_logfire() -> None:
    """Configure Logfire locally, without requiring a Logfire account/token."""
    try:
        logfire.configure(
            send_to_logfire=False,
            service_name="nba-rag-evaluation",
            console={"span_style": "simple"},
            inspect_arguments=False,
        )
        logfire.instrument_pydantic()
        logfire.instrument_pydantic_ai()
    except Exception as exc:
        logging.warning("Logfire could not be configured: %s", exc)
