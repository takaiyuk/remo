from datetime import datetime
from pathlib import Path

import gspread
import structlog
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

from remo.remo import DeviceTemperature

logger = structlog.get_logger(__name__)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def get_sheet_client(sheet_filename: str, secret_json_path: Path) -> Worksheet:
    # use creds to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret_json_path, scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_filename).sheet1
    return sheet


def is_temperature_updated(sheet_client: Worksheet, device_temperature: DeviceTemperature) -> bool:
    sheet_values: list[list[str]] = sheet_client.get_all_values()
    if not sheet_values:
        return True
    last_row = sheet_values[-1]
    last_val = float(last_row[0])
    last_created_at = last_row[1]
    return last_val != device_temperature.val or last_created_at != format_datetime(
        device_temperature.created_at
    )


def write_sheet(
    env_dict: dict[str, str], device_temperature: DeviceTemperature, verbose: bool = True
) -> None:
    sheet_client = get_sheet_client(env_dict["SHEET_FILENAME"], Path(env_dict["SECRET_JSON_PATH"]))
    if is_temperature_updated(sheet_client, device_temperature):
        row = [device_temperature.val, format_datetime(device_temperature.created_at)]
        index = len(sheet_client.get_all_values()) + 1
        sheet_client.insert_row(row, index)
        if verbose:
            logger.info(f"Insert row: {row}")
    else:
        logger.info("Temperature is not updated")
