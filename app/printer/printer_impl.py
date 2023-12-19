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
        _logger.info("SUMATRAPDF_EXECUTABLE: %s", sumatra_exe)

        if not sumatra_exe or not Path(sumatra_exe).is_file():
            raise ValueError("SUMATRAPDF_EXECUTABLE does not exists.")

        try:
            write_to_temp_success = True

            if file.filename.endswith(".pdf"):
                suffix = Path(file.filename).suffix
                with (NamedTemporaryFile(delete=True, suffix=suffix)) as temp:
                    shutil.copyfileobj(file.file, temp)
                    printable_path = Path(temp.name)
        except Exception as e:
            _logger.exception(e)
            write_to_temp_success = False
        finally:
            file.file.close()

        if not write_to_temp_success:
            raise Exception("Failed to write temporary PDF file.")

        code = subprocess.call([sumatra_exe,
                                "-silent", "-exit-when-done",
                                "-print-to-default",
                                "-print-settings", str(n_copies) + "x",
                                str(printable_path)])

        return code == 0


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
