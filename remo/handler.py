import os
from pathlib import Path
from typing import Any

from remo.remo import get_device_temperature
from remo.slack import SlackClient
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
            "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL"),
            "SLACK_CHANNEL": os.getenv("SLACK_CHANNEL"),
            "SLACK_ICON_EMOJI": os.getenv("SLACK_ICON_EMOJI"),
            "SLACK_USERNAME": os.getenv("SLACK_USERNAME"),
        }
    else:
        env_dict = read_env(Path(".env"))
    device_temperature = get_device_temperature(env_dict["TOKEN"], env_dict["DEVICE_NAME"])
    is_written = write_sheet(env_dict, device_temperature, verbose=True)
    if is_written:
        slack_client = SlackClient(
            webhook_url=env_dict["SLACK_WEBHOOK_URL"],
            channel=env_dict["SLACK_CHANNEL"],
            icon_emoji=env_dict["SLACK_ICON_EMOJI"],
            username=env_dict["SLACK_USERNAME"],
        )
        slack_client.notify(device_temperature)


def lambda_handler(event: Any, context: Any) -> dict[str, Any]:
    main()
    return {"statusCode": 200, "body": "OK"}
