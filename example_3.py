import subprocess
from pathlib import Path

sample_pdf = Path(__file__).parent / "libs" / "blank.pdf"
sumatra_pdf = Path(__file__).parent / "libs" / "SumatraPDF.exe"
printer_name = "Canon G1020 series HTTP"

try:
    subprocess.call([str(sumatra_pdf), "-print-to", printer_name,
                    "-print-settings", "2x", str(sample_pdf)])
except Exception as e:
    print(e)
