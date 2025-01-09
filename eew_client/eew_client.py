# encoding: utf-8
""" EEWのクライアントを提供するモジュール """
from typing import Callable

from websocket import WebSocket

from .axis_client import AXISClient, analyze_eew_info_axis
from .data_format import EEWInfo


class EEWClient:
    """EEW配信サービスのクライアント"""

    def __init__(
        self,
        func_get_eew_info: Callable[[EEWInfo], None] = None,
        eew_service_name: str = "",
        web_socket_func_open: Callable[[WebSocket], None] = None,
        web_socket_func_error: Callable[[WebSocket], None] = None,
        web_socket_func_close: Callable = None,
        debug: bool = False,
    ):

        self.axis = None

        if eew_service_name == "axis":
            if func_get_eew_info is None:
                on_message = None
            else:

                def on_message(
                    ws: WebSocket, message: str
                ):  # pylint: disable=unused-argument
                    eew_info_dataclass = analyze_eew_info_axis(message)
                    return func_get_eew_info(eew_info_dataclass)

            self.axis = AXISClient(
                web_socket_func_open=web_socket_func_open,
                web_socket_func_message=on_message,
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
