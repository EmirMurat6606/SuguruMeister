"""
This module contains the Suguru class and its methods.
It is used to create and manipulate Suguru puzzles.
@file: suguru.py
@brief: Suguru class and methods
@author: Emir Murat
@date: 2025-04-11
"""
import copy
import random

# Standard Suguru formats
# These are inspired by the https://Denksport.com Tectonic puzzles.
standard_formats = ["5x4", "11x4", "5x9", "11x9"]

# Difficulty levels
difficulties = ["easy", "medium", "hard"]


def check_format(su_format: str) -> tuple[int, int]:
    """
    Checks if the format is valid.
    :param: su_format: The format (represented as a string) to check.
    :return: A tuple containing the number of rows and columns.
    :raise: ValueError: If the format is not valid.
    """

    if su_format not in standard_formats:
        raise ValueError(f"Invalid format: {su_format}. Valid formats are: {standard_formats}")
    return int(su_format.split("x")[0]), int(su_format.split("x")[1])


def check_difficulty(difficulty: str) -> None:
    """
    Checks if the difficulty is valid.
    :param: difficulty: The difficulty level to check.
    :raise: ValueError: If the difficulty is not valid.
    """
    if difficulty not in difficulties:
        raise ValueError(f"Invalid difficulty: {difficulty}. Valid difficulties are: {difficulties}")


class Suguru:
    def __init__(self, su_format: str, difficulty: str) -> None:
        """
        Initializes the Suguru object with the given format.
        :param su_format: The format of the Suguru puzzle (Supported: 5x4, 5x9, 11x4, 11x9).
        :param difficulty: The difficulty level of the Suguru puzzle (Supported: easy, medium, hard).
        """
        row_col = check_format(su_format)
        check_difficulty(difficulty)
        self.rows: int = row_col[0]
        self.cols: int = row_col[1]
        self.difficulty = difficulty
        self.grid: list[list[int]] = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.regions: list["Region"] = []

    def __str__(self) -> str:
        """
        Returns a string representation of the Suguru object.
        :return: string representation
        """
        return f"Suguru({self.rows}x{self.cols}, {self.difficulty})"

    def print(self) -> None:
        """
        Prints the suguru grid.
        :return: None
        """
        print("Format: " + str(self.rows) + "x" + str(self.cols))
        print("Grid:")

        max_len = max(
            len(str(cell)) for row in self.grid for cell in row if cell is not None
        ) if any(cell is not None for row in self.grid for cell in row) else 1

        for row in self.grid:
            row_str = " ".join(
                f"{str(cell).rjust(max_len) if cell is not None else '.' * max_len}"
                for cell in row
            )
            print(row_str)

    def add_regions(self, regions: list["Region"]) -> None:
        """
        Adds a region to the Suguru object.
        :param regions: The region to add.
        """
        self.regions = regions
        for region in regions:
            for cell in region.cells:
                self.grid[cell[0]][cell[1]] = region.name


class Region:
    def __init__(self, name: str, size: int = 100):
        self.name: str = name
        self.size: int = size
        self.cells = set()

    def __str__(self):
        return f"Region {self.name}: {self.cells}"

    def has_cell(self, cell: tuple[int, int]):
        """
        Checks if the given cell is in the region.
        :param: cell: The cell to check.
        :return: True if the cell is in the region, False otherwise.
        """
        return cell in self.cells

    def add_cell(self, cell: tuple[int, int]) -> None:
        """
        Adds a cell to the region.
        :param: cell: The cell to add.
        """
        if self.cells.__len__() >= self.size:
            print("Region is full")
            return
        self.cells.add(cell)


def get_neighbors(cell: tuple[int, int], max_rows: int, max_cols: int) -> list[tuple[int, int]]:
    """
    Returns the neighbors of a cell in a 2D grid.
    :param cell: the cell to get neighbors for
    :param max_rows:
    :param max_cols:
    :return:
    """
    row, col = cell
    neighbors = []
    for dir_r, dir_c in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
        nr, nc = row + dir_r, col + dir_c
        if 0 <= nr < max_rows and 0 <= nc < max_cols:
            neighbors.append((nr, nc))
    return neighbors


def resolve_region(region: Region, current_cell, cells: set[tuple[int, int]]) -> bool:
    """
    Checks if a region can locally be expanded. If not, the region is complete and size is shrunk.
    :param region: the region to check
    :param current_cell: the current cell of the region
    :param cells: the cells that are not yet in a region
    :return: True if the region is complete, False otherwise
    """
    if (current_cell[0] - 1, current_cell[1]) not in cells and (current_cell[0] + 1, current_cell[1]) not in cells and (
    current_cell[0], current_cell[1] - 1) not in cells and (current_cell[0], current_cell[1] + 1) not in cells:
        region.size = region.cells.__len__()
        return True
    return False

def check_neighbours(suguru: Suguru, row: int, col: int):
    """
    Check if all surrounding cells have a different value
    :param suguru: The Suguru object.
    :param row: The row of the cell.
    :param col: The column of the cell.
    :return: True if the neighbors are valid, False otherwise.
    """
    neighbors = get_neighbors((row, col), suguru.rows, suguru.cols)
    for neighbor in neighbors:
        if suguru.grid[neighbor[0]][neighbor[1]] == suguru.grid[row][col]:
            return True
    return False

def count_numbers(suguru: Suguru) -> bool:
    """
    Checks if the appearance of numbers is valid
    :param suguru: the suguru to check
    :return: True if the numbers are valid, False otherwise
    """
    number_counts = dict()
    for i in range(suguru.rows):
        for j in range(suguru.cols):
            number_counts[suguru.grid[i][j]] = number_counts.get(suguru.grid[i][j], 0) + 1

    return number_counts[1] >= number_counts[2] >= number_counts[3] >= number_counts[4] >= number_counts[5]

def fill_grid(suguru: Suguru, row: int, col: int):
    """
    Recursive function to fill the Suguru grid.
    :param suguru: The Suguru object that is being modified
    :param row: The current row.
    :param col: The current column.
    """

    if row == suguru.rows:
        return count_numbers(suguru)

    next_row = row + (col + 1) // suguru.cols
    next_col = (col + 1) % suguru.cols

    not_used = [1, 2, 3, 4, 5]
    while not_used.__len__() > 0:
        num = random.choice(not_used)
        not_used.remove(num)
        suguru.grid[row][col] = num

        if not check_neighbours(suguru, row, col):
            if fill_grid(suguru, next_row, next_col):
                return True

    suguru.grid[row][col] = 0
    return False


def generate_suguru(su_format: str, difficulty: str) -> Suguru:
    """
    Generates a Suguru puzzle with the given format and difficulty. The maximum region size is 5.
    :param su_format: The format of the Suguru puzzle (Supported: 5x4, 5x9, 11x4, 11x9).
    :param difficulty: The difficulty level of the Suguru puzzle (Supported: easy, medium, hard).
    :return: A Suguru object with the generated puzzle.
    """

    # Initialize the Suguru
    suguru = Suguru(su_format, difficulty)

    # Fill the grid with random numbers
    fill_grid(suguru, 0, 0)

    # Divide grid into regions

    return suguru
