import logging
from typing import Annotated
from io import BytesIO

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import ENV
from app.services import get_printer_service

_logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def post_printer_print(file: Annotated[bytes, File()], filename: str, n_copies: int):
    try:
        printer = get_printer_service()
        success = printer.queue_print(filename, file, n_copies)
        return {
            "success": success
        }
    except Exception as e:
        _logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))

app.mount("/", StaticFiles(directory="html"), name="web")


# set credits

# get credits
