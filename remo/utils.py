import os
from pathlib import Path
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)

IS_AWS_LAMBDA_RUNTIME: bool = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None


def read_env(path: Path) -> dict[str, Optional[str]]:
    envs = {}
    with open(path, "r") as f:
        for x in f.readlines():
            key, val = x.split("=")
            if envs.get(key) is not None:
                raise KeyError(f"{key} is duplicated")
            val = val.strip()
            if val == "":
                logger.info(f"{key} is empty")
                val = None
            envs[key] = val
    return envs
