# encoding: utf-8
""" EEWのクライアントを提供するモジュール """
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable

from websocket import WebSocket

from .axis_client import AXISClient

INIT_DATETIME = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)


class IntensityEnum(Enum):
    """震度の列挙型"""

    LEVEL_0 = "0"
    LEVEL_1 = "1"
    LEVEL_2 = "2"
    LEVEL_3 = "3"
    LEVEL_4 = "4"
    LEVEL_5_MINUS = "5-"
    LEVEL_5_PLUS = "5+"
    LEVEL_6_MINUS = "6-"
    LEVEL_6_PLUS = "6+"
    LEVEL_7 = "7"
    OVER = "7より上"
    UNKNOWN = "不明"
    NO_DATA = "データなし"


@dataclass
class Hypocenter:
    """震源情報を格納するデータクラス"""

    code: int = -1  # 震源地コード
    name: str = ""  # 震源地名
    longitude: float = -1.0  # 経度
    latitude: float = -1.0  # 緯度
    depth: float = -1.0  # 深さ
    description: str = ""  # 整形済みの震源の説明


@dataclass
class Forcast:
    """予測情報を格納するデータクラス"""

    code: int = -1  # 予測地の地域コード
    name: str = ""  # 予測地の地域名
    max_intensity_lower: IntensityEnum = IntensityEnum.NO_DATA  # 予想最大震度の下限
    max_intensity_upper: IntensityEnum = IntensityEnum.NO_DATA  # 予想最大震度の上限
    description: str = ""  # 整形済みの最大深度の説明
    time: datetime = INIT_DATETIME  # 予測地の地震到達予想時刻


@dataclass
class EEWInfo:
    """EEW情報を格納するデータクラス"""

    title: str = ""  # タイトル
    origin_time: datetime = INIT_DATETIME  # 地震発生時刻
    announced_time: datetime = INIT_DATETIME  # EEW発表時刻
    event_id: str = ""  # 地震ID
    serial: int = -1  # 報番号
    hypocenter: Hypocenter = field(default_factory=Hypocenter)  # 震源情報
    max_intensity: IntensityEnum = IntensityEnum.NO_DATA  # 最大震度
    max_magunitude: float = -1.0  # 最大震度
    is_final: bool = False  # 最終報かどうか
    is_cancel: bool = False  # キャンセル報かどうか
    is_training: bool = False  # 訓練報かどうか
    supplementary_text: str = ""  # 補足情報


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
                on_message = func_get_eew_info(self.get_eew_info_axis)
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

    def get_eew_info_axis(self, eew_message: dict) -> EEWInfo:
        """AXISのサーバーから受け取ったEEW情報を解析する

        Args:
            eew_message (dict): web socketで受け取ったメッセージ

        Returns:
            EEWInfo: EEW情報を格納したデータクラス
        """
        eew_info_data = EEWInfo()

        eew_info_data.title = eew_message["title"]
        return eew_info_data

    def run_forever(self):
        """サーバーとの通信を継続する"""
        self.axis.run_forever()
