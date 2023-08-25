class SudokuSolver:
    @staticmethod
    def solve(board, x=0, y=0):
        backtrack_cnt = 0

        x, y = SudokuSolver.find_next_cell_to_fill(board, x, y)
        if x == -1:
            return True, backtrack_cnt

        for e in range(1, board.size + 1):
            board.set_cell(y, x, e)
            backtrack_cnt += 1
            if len(board.get_invalid_cells()) == 0:
                is_solved, steps = SudokuSolver.solve(board, x, y)
                backtrack_cnt += steps

                if is_solved:
                    return True, backtrack_cnt

            # Undo the current cell for backtracking
            board.set_cell(y, x, 0)

        return False, backtrack_cnt

    @staticmethod
    def find_next_cell_to_fill(board, i, j):
        for x in range(i, board.size):
            for y in range(j if x == i else 0, board.size):
                if board.get_cell(y, x) == 0:
                    return x, y

        return -1, -1
