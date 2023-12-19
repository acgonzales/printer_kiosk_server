import time
import logging
import subprocess
import shutil
import os
from tempfile import NamedTemporaryFile
from pathlib import Path

from fastapi import UploadFile

from app.printer.printer import Printer

_logger = logging.getLogger(__name__)

PRINTER_NAME = "Canon G1020 series HTTP"


class PrinterImplSumatra(Printer):
    def get_active_printer(self):
        _logger.info("PrinterImplSumatra.get_active_printer() called.")
        return PRINTER_NAME

    def queue_print(self, file: UploadFile, n_copies: int):
        _logger.info(
            "PrinterImplSumatra.queue_print() called. file=%s, n_copies=%s", file.filename, n_copies
        )

        sumatra_exe = os.getenv("SUMATRAPDF_EXECUTABLE")
        _logger.info("SUMATRAPDF_EXECUTABLE=%s", sumatra_exe)

        if not sumatra_exe or not Path(sumatra_exe).is_file():
            raise ValueError("SUMATRAPDF_EXECUTABLE does not exists.")

        success = False

        try:
            if file.filename.endswith(".pdf"):
                suffix = Path(file.filename).suffix
                with (NamedTemporaryFile(delete=True, suffix=suffix)) as temp:
                    shutil.copyfileobj(file.file, temp)
                    printable_path = Path(temp.name)
                    _logger.info(
                        "Generated Temporary PDF file=%s", printable_path)

                    code = subprocess.call([sumatra_exe,
                                            "-silent", "-exit-when-done",
                                            "-print-to", PRINTER_NAME,
                                            "-print-settings", str(
                                                n_copies) + "x",
                                            str(printable_path)])

                    success = code == 0
        except Exception as e:
            _logger.exception(e)
        finally:
            file.file.close()
            return success


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
