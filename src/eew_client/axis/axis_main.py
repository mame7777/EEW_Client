import json
from logging import Logger

import requests
import websocket
from requests import Response

from ..settings import Settings
from ..type import BaseClient


class AxisClient(BaseClient):
    def __init__(self, settings: Settings, logger: Logger):
        self.logger = logger
        self.settings = settings
        self._check_settings()
        self.access_token: str = settings.axis_access_token
        self.server_list_api_url: str = settings.axis_server_list_api_url
        self.token_refresh_api_url: str = settings.axis_token_refresh_api_url
        self.server_list: list[str] = []
        self.ws = None

    def _check_settings(self) -> None:
        if not self.settings.axis_access_token:
            raise ValueError("Axis access token is not set.")
        if not self.settings.axis_server_list_api_url:
            raise ValueError("Axis server list API URL is not set.")
        if not self.settings.axis_token_refresh_api_url:
            raise ValueError("Axis token refresh API URL is not set.")
        self.logger.debug("Axis settings are valid.")
        return None

    def _get_server_list(self) -> None:
        try:
            response: Response = requests.get(
                self.server_list_api_url,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=6.0,
            )
            if response.status_code != 200:

                raise ValueError(f"Failed to fetch server list: {response.status_code}")
            response_json: dict = json.loads(response.text)
            server_list: list[str] = response_json.get("servers", [])
            if len(server_list) == 0:
                raise ValueError("Server list is empty.")
            self.logger.debug(f"Server list: {server_list}")
            self.server_list = server_list
        except requests.RequestException as e:
            print(f"Error fetching server list: {e}")
        return None

    def run(self):
        self._get_server_list()
        for server_url in self.server_list:
            try:
                self.ws = websocket.WebSocketApp(
                    f"{server_url}/socket",
                    header=[f"Authorization: Bearer {self.access_token}"],
                    # on_open=self._private_on_open,
                    # on_message=self._private_on_message,
                    # on_error=self._private_on_error,
                    # on_close=self._private_on_close,
                )
            except Exception as e:
                print(f"[Error] cannot connect to {server_url}\n{e}")
                continue
