"""
@file: suguru_exporter.py
@brief: Suguru exporter class and methods
@author: Emir Murat
@date: 2025-04-11
@details: This file contains the SuguruExporter class and methods for exporting Suguru puzzles to various formats.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.suguru import check_format, check_difficulty

# Specify the output path for the exported files
standard_path = "outputs/suguru_puzzles.pdf"


class SuguruExporter:
    """
    This class is responsible for exporting Suguru puzzles to various formats.
    """

    @staticmethod
    def export_to_pdf(input_file: str, output_path: str = standard_path) -> None:
        """
        Exports the Suguru puzzle to a PDF file based on a regular text file.
        The puzzles are randomly generated and ordered in the pdf file.

        Input file format:
            - The input file should contain a description of amount of puzzles, size of each puzzle, and the difficulty level.
            - Format: <size> <difficulty> <amount> (without brackets)
            - Separate every statement with a new line
            - You can specify a combination of sizes and difficulties that are valid
            - Example: 5x4 easy 3

        :param input_file: input file path
        :param output_path: output file path
        :return: None
        """

        # Check if the input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} not found.")

        # Read input file and check for valid format
        with open(input_file, "r") as file:
            lines = file.readlines()
            puzzles = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ")
                if len(parts) != 3:
                    raise ValueError(f"Invalid format in line: {line}. Expected format: <size> <difficulty> <amount>")

                size, difficulty, amount = parts
                print(parts)
                try:
                    amount = int(amount)
                except ValueError:
                    raise ValueError(f"Invalid amount: {amount}. Expected an integer.")

                # Validate size and difficulty
                check_format(size)
                check_difficulty(difficulty)

                # Generate puzzles
                for _ in range(amount):
                    puzzles.append((size, difficulty))

        # Export puzzles to PDF
        with open(output_path, "w") as file:
            for size, difficulty in puzzles:
                file.write(f"Size: {size}, Difficulty: {difficulty}\n")



