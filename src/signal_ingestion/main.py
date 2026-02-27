"""Entry point for the signal ingestion service."""

import uvicorn

from shared.config import get_config


def main() -> None:
    config = get_config()
    uvicorn.run(
        "signal_ingestion.api:app",
        host=config["api_host"],
        port=config["api_port"],
        reload=False,
    )


if __name__ == "__main__":
    main()
