from pathlib import Path

import gspread
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials

from remo.remo import DeviceTemperature


def get_sheet_client(sheet_filename: str, secret_json_path: Path) -> Worksheet:
    # use creds to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret_json_path, scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_filename).sheet1
    return sheet


def write_sheet(
    env_dict: dict[str, str], device_temperature: DeviceTemperature, verbose: bool = True
) -> None:
    sheet_client = get_sheet_client(env_dict["SHEET_FILENAME"], Path(env_dict["SECRET_JSON_PATH"]))
    row = [device_temperature.val, device_temperature.created_at.strftime("%Y-%m-%dT%H:%M:%S")]
    index = len(sheet_client.get_all_values()) + 1
    sheet_client.insert_row(row, index)
    if verbose:
        print(row)
