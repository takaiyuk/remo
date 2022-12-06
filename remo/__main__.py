from pathlib import Path

from remo.remo import get_device_temperature
from remo.spreadsheet import get_sheet_client, write_sheet
from remo.utils import read_env


def main():
    env_dict = read_env(Path(".env"))
    device_temperature = get_device_temperature(env_dict["TOKEN"], env_dict["DEVICE_NAME"])
    sheet_client = get_sheet_client(env_dict["SHEET_FILENAME"], Path(env_dict["SECRET_JSON_PATH"]))
    write_sheet(sheet_client, device_temperature, verbose=True)


if __name__ == "__main__":
    main()
