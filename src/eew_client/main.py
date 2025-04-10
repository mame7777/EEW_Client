from logging import Logger, getLogger

from .axis.axis_main import AxisClient
from .settings import Settings

settings = Settings()


class EEWClient:
    """hogehoge"""

    def __init__(
        self, client_type: str, logger: Logger = None, debug: bool = False
    ) -> None:
        self.settings = settings
        self._on_message_callback = None
        self.logger = logger or getLogger(__name__)

        if debug or self.settings.debug:
            self.logger.setLevel("DEBUG")

        match client_type:
            case "axis":
                self.client = AxisClient(settings=self.settings, logger=self.logger)
            case "wolfx":
                self.client = None
            case _:
                raise ValueError(f"Unknown client type: {client_type}")
        self.client.run()

    def on_message(self, func) -> None:
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        self._on_message_callback = _wrapper
        return _wrapper

    def trigger_message(self, message: str) -> None:
        """Trigger the message callback."""
        if self._on_message_callback:
            self._on_message_callback(message)
            self.logger.debug(f"Triggered message: {message}")
