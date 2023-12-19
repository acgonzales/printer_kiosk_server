from abc import ABC, abstractmethod

from fastapi import UploadFile


class Printer(ABC):
    @abstractmethod
    def get_active_printer(self):
        pass

    @abstractmethod
    def queue_print(self, file: UploadFile, n_copies: int):
        pass
