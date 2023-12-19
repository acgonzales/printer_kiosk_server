import win32api
from pathlib import Path

source_file_name = Path.home() / "Downloads" / "blank.pdf"
win32api.ShellExecute(0, "print", str(source_file_name), None, ".", 0)
