import logging

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from app.config import ENV
from app.services import get_printer_service

_logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/", StaticFiles(directory="html"), name="web")


@app.get("/api/status")
async def get_status():
    return {
        "active": True,
        "env": ENV
    }


@app.get("/api/printer")
async def get_printer_status():
    try:
        printer = get_printer_service()
        return {
            "name": printer.get_active_printer()
        }
    except Exception as e:
        _logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/printer")
async def post_printer_print(file: UploadFile, n_copies: int):
    try:
        printer = get_printer_service()
        success = printer.queue_print(file, n_copies)
        return {
            "success": success
        }
    except Exception as e:
        _logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))

# set credits

# get credits
