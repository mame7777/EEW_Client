from abc import ABCMeta, abstractmethod
from logging import Logger

from .settings import Settings


class BaseClient(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, settings: Settings, logger: Logger, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    def run(self):
        pass
        pass
