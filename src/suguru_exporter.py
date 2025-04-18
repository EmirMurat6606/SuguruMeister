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
from src.suguru import check_format, check_difficulty, Suguru, generate_suguru

# Specify the output path for the exported files
standard_path = "outputs/suguru_puzzles.pdf"


def read_config(input_file: str) -> list:

    """
    Reads the input file for the Suguru puzzle configuration and returns Suguru puzzles.

    :param input_file: Path to the input file.
    :return: List of Suguru puzzles
    :raise: FileNotFoundError: If the input file does not exist.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} not found.")

    # Read input file and check for valid format
    with open(input_file, "r") as file:
        lines = file.readlines()
        formats = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ")
            if len(parts) != 3:
                raise ValueError(f"Invalid format in line: {line}. Expected format: <size> <difficulty> <amount>")

            size, difficulty, amount = parts
            try:
                amount = int(amount)
            except ValueError:
                raise ValueError(f"Invalid amount: {amount}. Expected an integer.")

            # Validate size and difficulty
            check_format(size)
            check_difficulty(difficulty)

            # Generate puzzles
            for _ in range(amount):
                formats.append((size, difficulty))

    puzzles = []
    for su_format, difficulty in formats:
        suguru = generate_suguru(su_format, difficulty)
        suguru.print()
        puzzles.append(suguru)

    return puzzles


class SuguruExporter:
    """
    This class is responsible for exporting Suguru puzzles to various formats.
    """

    @staticmethod
    def _draw_puzzle(my_canvas: canvas, puzzle: Suguru, x: int, y: int, cell_size: int = 30) -> None:
        """
        Draws the Suguru puzzle on the canvas.
        :param my_canvas: the canvas to draw on
        :param puzzle: the Suguru puzzle to draw
        :param x: x-coordinate of the top-left corner
        :param y: y-coordinate of the top-left corner
        :param cell_size: size of each cell
        :return: None
        """
        def get_region_of(cell):
            for region in puzzle.regions:
                if region.has_cell(cell):
                    return region
            return None

        for row in range(puzzle.rows):
            for col in range(puzzle.cols):


                cell_x = x + col * cell_size
                cell_y = y - row * cell_size

                value = puzzle.grid[row][col]
                if value != 0:
                    my_canvas.setFont("Helvetica", 10)
                    my_canvas.drawString(cell_x + 10, cell_y + 10, str(value))

                my_canvas.setLineWidth(0.5)
                my_canvas.rect(cell_x, cell_y, cell_size, cell_size)

                current_region = get_region_of((row, col))

                if col < puzzle.cols - 1:
                    right_region = get_region_of((row, col + 1))
                    if right_region.name != current_region.name:
                        my_canvas.setLineWidth(2)
                        my_canvas.line(
                            cell_x + cell_size, cell_y,
                            cell_x + cell_size, cell_y + cell_size
                        )


                if row < puzzle.rows - 1:
                    bottom_region = get_region_of((row + 1, col))
                    if bottom_region.name != current_region.name:
                        my_canvas.setLineWidth(2)
                        my_canvas.line(
                            cell_x, cell_y,
                            cell_x + cell_size, cell_y
                        )

        my_canvas.setLineWidth(2.5)
        my_canvas.rect(x, y - (puzzle.rows-1) * cell_size, puzzle.cols * cell_size, puzzle.rows * cell_size)

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

        # Parse file
        puzzles = read_config(input_file)

        # Export puzzles to PDF
        my_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=1)
        width, height = A4

        title = "Suguru Puzzles"
        my_canvas.setTitle(title)
        my_canvas.setFont("Helvetica-Bold", 24)
        title_width = my_canvas.stringWidth(title, "Helvetica-Bold", 24)
        my_canvas.drawString((width - title_width) / 2, height - 50, title)

        my_canvas.setFont("Helvetica", 12)
        y = height - 100

        for puzzle in puzzles:
            cell_size = 30
            if y - puzzle.cols * cell_size <= 0:
                my_canvas.showPage()
                y = height - 100
            SuguruExporter._draw_puzzle(my_canvas, puzzle, (width - puzzle.cols * cell_size)/2, y)

            if y - 200 <= 0:
                my_canvas.showPage()
                y = height - 100
            else:
                y-= 200

        footer = "Generated by SuguruMeister - Author: Emir Murat"
        my_canvas.setFont("Helvetica", 8)
        footer_width = my_canvas.stringWidth(footer, "Helvetica", 8)
        my_canvas.drawString((width - footer_width) / 2, 20, footer)

        my_canvas.save()




