from abc import ABC, abstractmethod

from app.logging_util import get_logger
from app.lib.base_parser.exceptions import ParserException


class BaseParser(ABC):
    def __init__(self, html: str):
        self.html: str = html
        self.logger = get_logger(self.__class__.__name__)

    @property
    @abstractmethod
    def log_identity(self) -> dict:
        pass

    @abstractmethod
    def parse(self):
        pass

    def debug(self, message):
        extra = self.log_identity
        self.logger.info(message, extra=extra)

    def warning(self, warning_code: int, msg: str):
        extra = self.log_identity
        extra['warning_code'] = warning_code
        self.logger.warning(msg, extra=extra)

    def critical(self, error_code: int, msg: str):
        extra = self.log_identity
        extra['error_code'] = error_code
        self.logger.error(msg, extra=extra)
        raise ParserException(msg)

    def write_html_to_file(self, full_file_path: str):
        with open(full_file_path, 'w') as f:
            f.write(self.html)
