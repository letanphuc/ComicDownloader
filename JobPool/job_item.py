from .logger import get_logger
import importlib

_logger = get_logger(__name__)


class JobItem:
    def __init__(self, action, data):
        self.module = action.__module__
        self.action = action.__name__
        self.data = data

    def run(self):
        try:
            module = importlib.import_module(self.module)
            func = getattr(module, self.action)
            return func(self.data)
        except Exception as e:
            _logger.warn(f'Exception e = {e}')
        return None

    def __str__(self):
        return f'{self.__class__}: {self.action}, {self.data}'
