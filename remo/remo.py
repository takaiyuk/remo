from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

ENDPOINT_URL_DEVICES = "https://api.nature.global/1/devices"
HEADERS = {"accept": "application/json"}


@dataclass
class DeviceTemperature:
    val: float
    created_at: datetime


def get_device_temperature(token: str, device_name: str) -> DeviceTemperature:
    HEADERS.update({"Authorization": f"Bearer {token}"})
    # curl -X GET "https://api.nature.global/1/devices" -H "accept: application/json" -H "Authorization: Bearer {TOKEN}"
    r = requests.get(ENDPOINT_URL_DEVICES, headers=HEADERS)
    for device in r.json():
        if device["name"] == device_name:
            event = device["newest_events"]["te"]
            device_temperature = DeviceTemperature(
                val=event["val"],
                created_at=datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%S%z").astimezone(
                    ZoneInfo("Asia/Tokyo")
                ),
            )
            break
    return device_temperature
