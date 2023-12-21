from abc import ABC, abstractmethod
import io


class Printer(ABC):
    @abstractmethod
    def get_active_printer(self):
        pass

    @abstractmethod
    def queue_print(self, filename: str, file: io.BytesIO, n_copies: int):
        pass
