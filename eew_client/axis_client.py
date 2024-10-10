import datetime
import json
import os
import threading
import time

import requests
import websocket
from dotenv import load_dotenv


class AXISClient:
    """AXISのサーバーと通信するクライアント"""

    def __init__(
        self,
        web_socket_func_open=None,
        web_socket_func_message=None,
        web_socket_func_error=None,
        web_socket_func_close=None,
        debug: bool = False,
    ):

        self.debug = debug
        websocket.enableTrace(debug)
        self.ws = None

        if web_socket_func_open is not None:
            self.on_open = web_socket_func_open
        if web_socket_func_message is not None:
            self.on_message = web_socket_func_message
        if web_socket_func_error is not None:
            self.on_error = web_socket_func_error
        if web_socket_func_close is not None:
            self.on_close = web_socket_func_close

        self.is_connected = False

        self.is_reflesh_eew_api_token_at_end_of_month = True
        self.is_refleshed_eew_api_token = False

        load_dotenv()
        self.eew_access_token = os.environ["EEW_ACCESS_TOKEN"]
        self.eew_server_list_api_url = os.environ["EEW_SERVER_LIST_API_URL"]

    def on_message(self, ws: websocket.WebSocket, message):
        if not self.is_connected:
            if message == "hello":
                self.is_connected = True
                print("[Info] connected to server!")
            else:
                print("[Error] cannot connect to server!")
                raise ConnectionError()
        print(message)

    def on_error(self, ws: websocket.WebSocket, error):
        print(error)

    def on_close(self, ws: websocket.WebSocket, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws: websocket.WebSocket):
        print("### open ###")

    def get_server_list(self) -> list:
        """EEW情報を配信しているサーバリストを取得する

        Raises:
            ConnectionError: サーバーからのレスポンスが200以外
            ValueError: サーバーリストが取得できなかった

        Returns:
            list: サーバーのアドレスが入ったリスト
        """
        response = requests.get(
            self.eew_server_list_api_url,
            headers={"Authorization": "Bearer %s" % self.eew_access_token},
            timeout=6.0,
        )
        if response.status_code != 200:
            print("[Error] cannot connect server-list server!")
            raise ConnectionError()
        response_json = json.loads(response.text)
        server_list = response_json.get("servers", [])
        if len(server_list) < 1:
            print("[Error] cannot get server list!")
            raise ValueError()
        if self.debug:
            print(f"[Info] server list: {server_list}")
        return server_list

    def judge_need_reflesh_token(self) -> bool:
        """API Tokenを更新する必要があるかどうかを判定する

        Returns:
            bool: tokenを更新する必要があるかどうか
        """
        print("[Info] judge need reflesh token")
        return False

    def reflesh_token(self):
        """API Tokenをリフレッシュする"""
        print("[Info] reflesh token")

    def run_forever(self):
        """EEW情報を取得し続ける

        Raises:
            ConnectionError: サーバーに接続できない
        """
        server_list = self.get_server_list()
        for server_list_index in range(len(server_list)):
            server_url = server_list[server_list_index]
            try:
                self.ws = websocket.WebSocketApp(
                    "%s/socket" % server_url,
                    header=["Authorization: Bearer %s" % self.eew_access_token],
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                )
                break
            except:
                if server_list_index == len(server_list) - 1:
                    print("[Error] cannot connect to any server!")
                    raise ConnectionError()
                else:
                    continue
        if self.debug:
            print(f"[Info] connected to {server_url}")

        try:
            ws_thread = threading.Thread(
                target=self.ws.run_forever,
                kwargs={"ping_interval": 25},
                name="ws_thread",
            )
            ws_thread.start()
            start_datetime = datetime.datetime.now()
            while True:
                # プログラムを24hours止める
                time.sleep(3600 * 24)

                if (datetime.datetime.now() - start_datetime).seconds >= 3600 * 24:
                    if self.judge_need_reflesh_token():
                        self.reflesh_token()
                        start_datetime = datetime.datetime.now()

        except KeyboardInterrupt:
            self.ws.close()
        # error everything
        except:
            self.ws.close()
