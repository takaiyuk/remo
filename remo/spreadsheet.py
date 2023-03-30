from datetime import datetime
from pathlib import Path
from typing import Optional

import gspread
import structlog
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

from remo.remo import DeviceTemperature

logger = structlog.get_logger(__name__)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def get_sheet_client(sheet_filename: Optional[str], secret_json_path: Optional[Path]) -> Optional[Worksheet]:
    if sheet_filename is None or secret_json_path is None:
        return None
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
) -> bool:
    sheet_filename = env_dict["SHEET_FILENAME"]
    secret_json_path = Path(env_dict["SECRET_JSON_PATH"])
    sheet_client = get_sheet_client(sheet_filename, secret_json_path)
    if sheet_client is None:
        if verbose:
            if sheet_filename is None:
                logger.info("SHEET_FILENAME is not found")
            if secret_json_path is None:
                logger.info("SECRET_JSON_PATH is not found")
        return False
    if is_temperature_updated(sheet_client, device_temperature):
        row = [device_temperature.val, format_datetime(device_temperature.created_at)]
        index = len(sheet_client.get_all_values()) + 1
        sheet_client.insert_row(row, index)
        if verbose:
            logger.info(f"Insert row: {row}")
        return True
    else:
        if verbose:
            logger.info("Temperature is not updated")
        return False
