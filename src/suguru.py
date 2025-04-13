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
# These are used for generating the Suguru puzzles
standard_formats = ["5x4", "4x5"]

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


def check_difficulty(difficulty: str) -> str:
    """
    Checks if the difficulty is valid.
    :param: difficulty: The difficulty level to check.
    :raise: ValueError: If the difficulty is not valid.
    :return: the difficulty level (if valid)
    """
    if difficulty not in difficulties:
        raise ValueError(f"Invalid difficulty: {difficulty}. Valid difficulties are: {difficulties}")
    return difficulty

class Suguru:
    def __init__(self, su_format: str, difficulty: str) -> None:
        """
        Initializes the Suguru object with the given format.
        :param su_format: The format of the Suguru puzzle
        :param difficulty: The difficulty level of the Suguru puzzle (Supported: easy, medium, hard).
        """
        row_col = check_format(su_format)
        self.rows: int = row_col[0]
        self.cols: int = row_col[1]
        self.difficulty = check_difficulty(difficulty)
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
        Adds regions to the Suguru object.
        :param regions: The regions to add.
        """
        self.regions = regions
        for region in regions:
            for cell in region.cells:
                self.grid[cell[0]][cell[1]] = region.name


class Region:
    def __init__(self, name: str, cells: set[tuple[int, int]]) -> None:
        self.name: str = name
        self.cells: set = cells
        self.size: int = len(cells)

    def __str__(self):
        return f"Region {self.name}: {self.cells}"

    def has_cell(self, cell: tuple[int, int]):
        """
        Checks if the given cell is in the region.
        :param: cell: The cell to check.
        :return: True if the cell is in the region, False otherwise.
        """
        return cell in self.cells

    def add_cells(self, cells: list[tuple[int, int]]) -> None:
        """
        Adds a cell to the region.
        :param: cell: The cell to add.
        """
        self.cells = set(cells)
        self.size = len(self.cells)


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
    for dir_r, dir_c in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nr, nc = row + dir_r, col + dir_c
        if 0 <= nr < max_rows and 0 <= nc < max_cols:
            neighbors.append((nr, nc))
    return neighbors


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

def grow_region(suguru, cells, region, used_cells, candidates, available_numbers, target_size) -> bool:
    """
    Helper function to expand a region in the Suguru grid.
    :param suguru: the suguru object to modify
    :param cells: the cells that are not yet assigned to a region
    :param region: the current region being expanded
    :param used_cells: the cells that have already been used in the region
    :param candidates: the cells that can be used to expand the region
    :param available_numbers: the numbers that can be used to fill the region
    :param target_size: the target size of the region
    :return: bool, True if the region can be expanded to the target size, False otherwise
    """
    if not available_numbers:
        return True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(candidates)

    for r, c in candidates:
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if (0 <= nr < suguru.rows and 0 <= nc < suguru.cols and
                neighbor in cells and
                neighbor not in used_cells and
                suguru.grid[nr][nc] in available_numbers):

                value = suguru.grid[nr][nc]
                region.append(neighbor)
                used_cells.add(neighbor)
                new_candidates = candidates + [neighbor]
                new_available = available_numbers.copy()
                new_available.remove(value)

                if grow_region(suguru, cells, region, used_cells, new_candidates, new_available, target_size):
                    return True

                # Backtrack
                region.pop()
                used_cells.remove(neighbor)

    return False


def divide_regions(suguru: Suguru, cells, regions, counter) -> tuple[bool, dict]:
    """
    Divides the Suguru grid into regions.
    :param suguru: the suguru object to modify
    :param cells: the cells that are not yet assigned to a region
    :param regions: the regions that have been created so far
    :param counter: a counter used for naming the regions
    :return: bool, regions (True if all cells are assigned, False otherwise)
    """

    if not cells:
        return True, regions

    for number in reversed(range(1, 6)):
        for cell in cells:
            row, col = cell
            if suguru.grid[row][col] == number:
                region = [cell]
                used_cells = {cell}
                candidates = [(row, col)]
                available_numbers = list(range(1, number))

                success = grow_region(
                    suguru, cells.copy(), region, used_cells, candidates, available_numbers, number - 1
                )

                if success:
                    counter += 1
                    for c in region:
                        cells.remove(c)
                    regions[str(counter)] = region
                    solved, final_regions = divide_regions(suguru, cells, regions, counter)
                    if solved:
                        return True, final_regions
                    # Backtrack
                    for c in region:
                        cells.append(c)
                    del regions[str(counter)]
                    counter -= 1

    return False, regions

def generate_suguru(su_format: str, difficulty: str):
    """
    Generates a Suguru puzzle with the given format and difficulty. The maximum region size is 5.
    :param su_format: The format of the Suguru puzzle (Supported: 5x4, 5x9, 11x4, 11x9).
    :param difficulty: The difficulty level of the Suguru puzzle (Supported: easy, medium, hard).
    :return: A Suguru object with the generated puzzle.
    """
    # Initialize the Suguru
    suguru = Suguru(su_format, difficulty)
    print("Suguru initialized")
    print("---------------------")

    # Fill the grid with random numbers
    # fill_grid(suguru, 0, 0)
    # print("Suguru grid filled")
    # suguru.print()
    # print("---------------------")

    """
    4 1 3 4 5
    3 2 5 1 2
    4 1 3 4 5
    2 5 2 1 3
    """

    suguru.grid = [[4, 1, 3, 4, 5],
                   [3, 2, 5, 1, 2],
                   [4, 1, 3, 4, 5],
                   [2, 5, 2, 1, 3]]
    print("Suguru grid filled")
    suguru.print()
    print("---------------------")

    # Divide grid into regions
    regions = dict()
    cells = [(i, j) for i in range(suguru.rows) for j in range(suguru.cols)]
    regions = divide_regions(suguru, cells, regions, 0)[1]

    print("Suguru regions divided")
    print("---------------------")

    print(regions)
    # Convert the regions to Region objects
    new_regions = []
    for region in regions:
        new_region = Region(region, regions[region])
        new_regions.append(new_region)
    suguru.add_regions(new_regions)
    return suguru
