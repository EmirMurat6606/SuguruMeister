"""
@file: main.py
@brief: Main source file for the project
@author: Emir Murat
@date: 2025-04-11
@details: This file contains the main function and serves as the entry point for the project.
@note: This project is licensed under the MIT License.
"""

from src.suguru import Suguru, generate_suguru
from src.suguru_exporter import SuguruExporter


if __name__ == "__main__":
    SuguruExporter.export_to_pdf("input.txt")



