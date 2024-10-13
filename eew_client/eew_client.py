# encoding: utf-8
""" EEWのクライアントを提供するモジュール """

from axis_client import AXISClient
from dotenv import load_dotenv


class EEWClient:
    """EEW配信サービスのクライアント"""

    def __init__(
        self,
        eew_service_name: str = "",
        web_socket_func_open=None,
        web_socket_func_message=None,
        web_socket_func_error=None,
        web_socket_func_close=None,
        debug: bool = False,
    ):

        self.axis = None

        if eew_service_name == "axis":
            self.axis = AXISClient(
                web_socket_func_open=web_socket_func_open,
                web_socket_func_message=web_socket_func_message,
                web_socket_func_error=web_socket_func_error,
                web_socket_func_close=web_socket_func_close,
                debug=debug,
            )
        elif eew_service_name == "wolfx":
            raise ValueError("Not implemented yet.")
        elif eew_service_name == "":
            raise ValueError(
                "name of eew service is required.\nPlese set eew_service to 'axis' or 'wolfx'."
            )
        else:
            raise ValueError(
                "name of eew service is invalid.\nPlese set eew_service to 'axis' or 'wolfx'."
            )

        self.debug = debug

    def run_forever(self):
        """サーバーとの通信を継続する"""
        self.axis.run_forever()


if __name__ == "__main__":
    import os

    load_dotenv()
    eew_access_token = os.environ["EEW_ACCESS_TOKEN"]
    eew_server_list_api_url = os.environ["EEW_SERVER_LIST_API_URL"]
    eew_token_reflesh_api_url = os.environ["EEW_TOKEN_REFLESH_API_URL"]
    client = EEWClient(eew_service_name="axis", debug=True)
    client.axis.set_token_and_url(
        eew_access_token=eew_access_token,
        eew_server_list_api_url=eew_server_list_api_url,
        eew_token_reflesh_api_url=eew_token_reflesh_api_url,
    )
    client.run_forever()
    client.run_forever()
