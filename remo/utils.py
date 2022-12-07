import os
from pathlib import Path

IS_AWS_LAMBDA_RUNTIME: bool = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None


def read_env(path: Path) -> dict[str, str]:
    with open(path, "r") as f:
        return {x.split("=")[0]: x.split("=")[1].strip() for x in f.readlines()}
