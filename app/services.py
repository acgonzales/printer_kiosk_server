from app.config import ENV

_printer = None


def get_printer_service():
    global _printer
    if _printer is None:
        if ENV == "prod":
            from app.printer import PrinterImpl
            _printer = PrinterImpl()
        else:
            from app.printer import PrinterMock
            _printer = PrinterMock()

    return _printer
