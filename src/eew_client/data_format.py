# encoding: utf-8
"""EEWの各種データのフォーマットを提供するモジュール"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

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
    forecast_list: list[Forcast] = field(default_factory=list)  # 予測情報のリストS
