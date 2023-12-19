import time
import logging

from fastapi import UploadFile

from app.printer.printer import Printer

_logger = logging.getLogger(__name__)


class PrinterImpl(Printer):
    def get_active_printer(self):
        raise NotImplementedError()

    def queue_print(self, file: UploadFile, n_copies: int):
        raise NotImplementedError()


class PrinterMock(Printer):
    def get_active_printer(self):
        _logger.info("PrinterMock.get_active_printer() called.")
        return "Mock Printer"

    def queue_print(self, file: UploadFile, n_copies: int):
        _logger.info(
            "PrinterMock.queue_print() called. file=%s, n_copies=%s", file.filename, n_copies
        )
        time.sleep(2.5)
        return True
