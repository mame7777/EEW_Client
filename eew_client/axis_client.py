""" AXISのサーバーと通信するクライアントプログラム """

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
        else:
            self.on_open = self._private_on_open

        if web_socket_func_message is not None:
            self.on_message = web_socket_func_message
        else:
            self.on_message = self._private_on_message

        if web_socket_func_error is not None:
            self.on_error = web_socket_func_error
        else:
            self.on_error = self._private_on_error

        if web_socket_func_close is not None:
            self.on_close = web_socket_func_close
        else:
            self.on_close = self._private_on_close

        self.is_connected = False

        self.is_try_reflesh_eew_api_token_at_end_of_month = True
        self.is_refleshed_eew_api_token = False

        load_dotenv()
        self.eew_access_token = os.environ["EEW_ACCESS_TOKEN"]
        self.eew_server_list_api_url = os.environ["EEW_SERVER_LIST_API_URL"]

    def _private_on_message(
        self, ws: websocket.WebSocket, message
    ):  # pylint: disable=unused-argument
        """messageを受け取ったときのデフォルト処理\n
        AXISClientのインスタンスの引数にon_message関数がある場合はそちらを実行し、\n
        指定のon_message関数がない場合はデフォルトの関数を実行する

        Args:
            ws (websocket.WebSocket): websocketのインスタンス
            message (_type_): 受け取ったメッセージ

        Raises:
            ConnectionError: 接続前に正常接続のメッセージが来なかった場合
        """
        if not self.is_connected:
            if message == "hello":
                self.is_connected = True
                print("[Info] connected to server!")
            else:
                print("[Error] cannot connect to server!")
                raise ConnectionError()
        print(message)

    def _private_on_error(
        self, ws: websocket.WebSocket, error
    ):  # pylint: disable=unused-argument
        """エラーが発生したときのデフォルト処理\n
        AXISClientのインスタンスの引数にon_error関数がある場合はそちらを実行し、\n
        指定のon_error関数がない場合はデフォルトの関数を実行する

        Args:
            ws (websocket.WebSocket): websocketのインスタンス
            error (_type_): エラー内容
        """
        print(error)

    def _private_on_close(
        self, ws: websocket.WebSocket, close_status_code, close_msg
    ):  # pylint: disable=unused-argument
        """接続が切断されたときのデフォルト処理\n
        AXISClientのインスタンスの引数にon_close関数がある場合はそちらを実行し、\n
        指定のon_close関数がない場合はデフォルトの関数を実行する

        Args:
            ws (websocket.WebSocket): websocketのインスタンス
            close_status_code (_type_): クローズステータスコード
            close_msg (_type_): クローズメッセージ
        """
        print("### closed ###")

    def _private_on_open(
        self, ws: websocket.WebSocket
    ):  # pylint: disable=unused-argument
        """接続が開かれたときのデフォルト処理\n
        AXISClientのインスタンスの引数にon_open関数がある場合はそちらを実行し、\n
        指定のon_open関数がない場合はデフォルトの関数を実行する

        Args:
            ws (websocket.WebSocket): websocketのインスタンス
        """
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
            headers={"Authorization": f"Bearer {self.eew_access_token}"},
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
        API Toekの更新は25日以降に行う．
        15日までにこの関数が呼ばれた場合，更新済みフラグをFalseにする

        Returns:
            bool: tokenを更新する必要があるかどうか
        """
        if not self.is_try_reflesh_eew_api_token_at_end_of_month:
            return False

        today = datetime.datetime.today()
        if self.is_refleshed_eew_api_token:
            if today.day < 15:
                self.is_refleshed_eew_api_token = False
            return False
        elif today.day >= 25:
            return True
        else:
            return False

    def reflesh_token(self) -> int:
        """API Tokenをリフレッシュする"""

        ### トークンをリフレッシュする処理 ###
        new_api_token = "hogehoge"

        self.eew_access_token = new_api_token
        self.is_refleshed_eew_api_token = True
        print("[Info] refleshed token")
        return 0

    def manage_token(self):
        """API Tokenの管理を行う"""
        sleep_time = 3600 * 24
        while True:
            if self.is_try_reflesh_eew_api_token_at_end_of_month:
                break
            time.sleep(sleep_time)
            if self.judge_need_reflesh_token():
                self.reflesh_token()

    def run_forever(self):
        """EEW情報を取得し続ける

        Raises:
            ConnectionError: サーバーに接続できない
        """
        server_list = self.get_server_list()
        for server_url in server_list:
            try:
                self.ws = websocket.WebSocketApp(
                    f"{server_url}/socket",
                    header=[f"Authorization: Bearer {self.eew_access_token}"],
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                )
                if self.debug:
                    print(f"[Info] connected to {server_url}")
                break
            except Exception as e:
                print(f"[Error] cannot connect to {server_url}\n{e}")
                continue

        mng_api_token_thread = threading.Thread(
            target=self.manage_token,
            name="mng_api_token_thread",
            daemon=True,
        )
        mng_api_token_thread.start()
        try:
            self.ws.run_forever(ping_interval=25)
        except KeyboardInterrupt:
            self.ws.close()
        # error everything
        except Exception as e:
            print(f"[Error] {e}")
            self.ws.close()
            self.ws.close()
            self.ws.close()
