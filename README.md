SuguruMeister (In development)
==============================

This is a Python implementation of Suguru, a logic-based number puzzle. The goal of the game is to fill a grid such that
no number is adjacent to another number of the same value, and each number appears exactly once in each "region" of the
grid. The range of numbers is determined by the size of a grid (this particular implementation uses the numbers 1-5).

The current implementation is based on the well-known Tectonic puzzles of which you can find an example
at https://www.denksport.com

## Supported Features

- Creating a valid Suguru puzzle with a given format and difficulty level.
- Creating a pdf file with more valid puzzles. The structure (amount of puzzles of each kind) have to be defined in a
  configuration file. An example of this is provided in the `input.txt` file.

---

## Sizes and Difficulties

- The supported sizes are :
    - 5x4
    - 5x9
    - 11x4
    - 11x9
- Supported (standard) difficulties are:
    - Easy
    - Medium
    - Hard

---

## Installation

The packages required to run the code are listed in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt
```

To clone the repository, use the following command:

```bash
git clone https://github.com/EmirMurat6606/SuguruMeister.git
```

---