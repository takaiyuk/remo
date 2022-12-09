import json
from dataclasses import dataclass
from typing import Optional

import requests

from remo.remo import DeviceTemperature


@dataclass
class SlackSettings:
    webhook_url: str
    channel: str
    icon_emoji: Optional[str]
    username: Optional[str]


class SlackClient:
    def __init__(
        self, webhook_url: str, channel: str, icon_emoji: Optional[str] = None, username: Optional[str] = None
    ):
        self.settings = SlackSettings(
            webhook_url=webhook_url,
            channel=channel,
            icon_emoji=icon_emoji,
            username=username,
        )

    def notify(self, device_temperature: DeviceTemperature) -> None:
        message = self._build_message(device_temperature)
        self._post_slack(message)

    def _build_message(self, device_temperature: DeviceTemperature) -> str:
        return f"Device temperature: {device_temperature.val}℃"

    def _post_slack(self, message: str) -> None:
        data = json.dumps(self._slack_data(message))
        requests.post(self.settings.webhook_url, data)

    def _slack_data(self, message: str) -> dict:
        return {
            "username": self.settings.username,
            "icon_emoji": self.settings.icon_emoji,
            "channel": self.settings.channel,
            "text": message,
        }
