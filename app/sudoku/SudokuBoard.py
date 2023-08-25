from __future__ import annotations
import math
from typing import List


class SudokuBoard:

    def __init__(self, size: int):
        self._size = size
        self._box_size = math.isqrt(self._size)
        if self._box_size * self._box_size != self._size:
            raise Exception("Size must be the square of some number!")

        self._cells = [[0] * self._size for _ in range(self._size)]

    def set_cell_by_num(self, cell_num: int, value: int) -> None:
        self._cells[cell_num // self._size][cell_num % self._size] = value

    def set_cell(self, row: int, column: int, value: int) -> None:
        self._cells[row][column] = value

    def get_cell_by_num(self, cell_num: int) -> int:
        return self._cells[cell_num // self._size][cell_num % self._size]

    def get_cell(self, row: int, column: int) -> int:
        return self._cells[row][column]

    def clear(self) -> None:
        self._cells = [[0] * self._size for _ in range(self._size)]

    def swap_row(self, first_row: int, second_row: int) -> None:
        for x in range(0, self._size):
            temp = self._cells[first_row][x]
            self._cells[first_row][x] = self._cells[second_row][x]
            self._cells[second_row][x] = temp

    def swap_column(self, first_column: int, second_column: int) -> None:
        for y in range(0, self._size):
            temp = self._cells[y][first_column]
            self._cells[y][first_column] = self._cells[y][second_column]
            self._cells[y][second_column] = temp

    def swap_big_row(self, first_row: int, second_row: int) -> None:
        for y in range(0, self.box_size):
            self.swap_row(first_row * self.box_size + y, first_row * self.box_size + y)

    def swap_big_column(self, first_column: int, second_column: int) -> None:
        for x in range(0, self.box_size):
            self.swap_column(first_column * self.box_size + x, second_column * self.box_size + x)

    def get_invalid_cells(self) -> List[int]:
        invalid_cells = []

        for x in range(self._size):
            digits_count = [[] for i in range(self._size)]

            for y in range(self._size):
                cell_number = self._cells[y][x]
                if cell_number != 0:
                    digits_count[cell_number - 1].append(y * self._size + x)

            for cells in digits_count:
                if len(cells) > 1:
                    invalid_cells += cells

        for y in range(self._size):
            digits_count = [[] for i in range(self._size)]

            for x in range(self._size):
                cell_number = self._cells[y][x]
                if cell_number != 0:
                    digits_count[cell_number - 1].append(y * self._size + x)

            for cells in digits_count:
                if len(cells) > 1:
                    invalid_cells += cells

        for subgrid_x in range(0, self.size // self.box_size):
            for subgrid_y in range(0, self.size // self.box_size):
                digits_count = [[] for i in range(self.size)]

                for y in range(0, self.box_size):
                    for x in range(0, self.box_size):
                        cell_y = y + subgrid_y * self.box_size
                        cell_x = x + subgrid_x * self.box_size
                        cell_number = self._cells[cell_y][cell_x]
                        if cell_number != 0:
                            digits_count[cell_number - 1].append(cell_y * self._size + cell_x)

                for cells in digits_count:
                    if len(cells) > 1:
                        invalid_cells += cells

        return list(set(invalid_cells))

    @property
    def size(self) -> int:
        return self._size

    @property
    def box_size(self) -> int:
        return self._box_size

    @property
    def cell_count(self) -> int:
        return self._size * self._size

    @staticmethod
    def from_array(size: int, arr: List[int]) -> SudokuBoard:
        board = SudokuBoard(size)

        for i, val in enumerate(arr):
            board.set_cell_by_num(i, val)

        return board

    @staticmethod
    def box_size_from_board_size(size: int) -> int:
        return math.isqrt(size)

    @staticmethod
    def validate_board_size(size: int) -> bool:
        sqrt = math.isqrt(size)
        return sqrt * sqrt == size

    def to_array(self) -> List[int]:
        arr = []

        for i in range(self.cell_count):
            arr.append(self.get_cell_by_num(i))

        return arr
