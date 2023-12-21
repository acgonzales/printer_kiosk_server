from app.config import ENV, PROD_ENV

_printer = None


def get_printer_service():
    global _printer
    if _printer is None:
        if True or ENV == PROD_ENV:
            from app.printer import PrinterImplSumatra
            _printer = PrinterImplSumatra()
        else:
            from app.printer import PrinterMock
            _printer = PrinterMock()

    return _printer
