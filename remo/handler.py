import os
from pathlib import Path
from typing import Any

from remo.remo import get_device_temperature
from remo.spreadsheet import write_sheet
from remo.utils import IS_AWS_LAMBDA_RUNTIME, read_env


def main():
    """Write device temperature to Google Sheet"""
    if IS_AWS_LAMBDA_RUNTIME:
        env_dict = {
            "TOKEN": os.getenv("TOKEN"),
            "DEVICE_NAME": os.getenv("DEVICE_NAME"),
            "SHEET_FILENAME": os.getenv("SHEET_FILENAME"),
            "SECRET_JSON_PATH": os.getenv("SECRET_JSON_PATH"),
        }
    else:
        env_dict = read_env(Path(".env"))
    device_temperature = get_device_temperature(env_dict["TOKEN"], env_dict["DEVICE_NAME"])
    write_sheet(env_dict, device_temperature, verbose=True)


def lambda_handler(event: Any, context: Any) -> dict[str, Any]:
    main()
    return {"statusCode": 200, "body": "OK"}
