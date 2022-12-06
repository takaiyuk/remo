from pathlib import Path


def read_env(path: Path) -> dict[str, str]:
    with open(path, "r") as f:
        return {x.split("=")[0]: x.split("=")[1].strip() for x in f.readlines()}
