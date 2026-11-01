"""Verify the generated report with Microsoft Word: page count and PDF export."""

from __future__ import annotations

import sys
from pathlib import Path

import win32com.client

HERE = Path(__file__).resolve().parent
DOCX = HERE / "IoT_AI_Content_Generation_Mini_Project_Report_Teguia_Frank.docx"
PDF = HERE / "IoT_AI_Content_Generation_Mini_Project_Report_Teguia_Frank.pdf"


def main() -> int:
    if not DOCX.exists():
        raise SystemExit(f"missing {DOCX}")

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(str(DOCX), ReadOnly=True, AddToRecentFiles=False)
        doc.Repaginate()
        pages = doc.ComputeStatistics(2)  # wdStatisticPages
        words = doc.ComputeStatistics(0)  # wdStatisticWords
        chars = doc.ComputeStatistics(3)  # wdStatisticCharacters
        print(f"pages={pages}")
        print(f"words={words}")
        print(f"characters={chars}")

        if PDF.exists():
            PDF.unlink()
        doc.SaveAs(str(PDF), FileFormat=17)  # wdFormatPDF
        print(f"pdf={PDF}")
        doc.Close(SaveChanges=False)
    finally:
        word.Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
