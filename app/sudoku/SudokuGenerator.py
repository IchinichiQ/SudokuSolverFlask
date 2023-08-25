import random

from sudoku.SudokuBoard import SudokuBoard


class SudokuGenerator:
    @staticmethod
    def generate_solved_sudoku(size: int) -> SudokuBoard:
        sudoku_board = SudokuBoard(size)

        cur_line = [[i * sudoku_board.box_size + j for j in range(1, sudoku_board.box_size + 1)] for i in
                    range(0, sudoku_board.box_size)]

        for y in range(0, sudoku_board.size):
            for x in range(0, sudoku_board.size):
                sudoku_board.set_cell_by_num(y * sudoku_board.size + x,
                                             cur_line[x // sudoku_board.box_size][x % sudoku_board.box_size])

            cur_line = cur_line[1:] + cur_line[:1]
            if (y + 1) % sudoku_board.box_size == 0:
                for i in range(0, len(cur_line)):
                    cur_line[i] = cur_line[i][1:] + cur_line[i][:1]

        return sudoku_board

    @staticmethod
    def generate_random_sudoku(size: int, empty_cells_percent: float) -> SudokuBoard:
        solved_sudoku = SudokuGenerator.generate_solved_sudoku(size)

        iterations = size * 20
        actions = random.choices([0, 1, 2, 3], k=iterations)
        block_count = solved_sudoku.size // solved_sudoku.box_size
        for action in actions:
            blocks_to_swap = [random.randint(0, block_count - 1), random.randint(0, block_count - 1)]
            elements_to_swap = [
                blocks_to_swap[0] * solved_sudoku.box_size + random.randint(0, solved_sudoku.box_size - 1),
                blocks_to_swap[0] * solved_sudoku.box_size + random.randint(0, solved_sudoku.box_size - 1)]

            match action:
                case 0:
                    solved_sudoku.swap_row(elements_to_swap[0], elements_to_swap[1])
                case 1:
                    solved_sudoku.swap_column(elements_to_swap[0], elements_to_swap[1])
                case 2:
                    solved_sudoku.swap_big_row(blocks_to_swap[0], blocks_to_swap[1])
                case 3:
                    solved_sudoku.swap_big_column(blocks_to_swap[0], blocks_to_swap[1])

        cells_num = int(solved_sudoku.cell_count * empty_cells_percent)
        cells_idx = random.sample(range(0, solved_sudoku.cell_count), cells_num)
        for i in cells_idx:
            solved_sudoku.set_cell_by_num(i, 0)

        return solved_sudoku
