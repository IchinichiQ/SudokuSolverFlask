import math
from typing import List

from marshmallow import ValidationError
from marshmallow.types import Validator


class BoardValidator(Validator):
    def __call__(self, board: List[int]) -> List[int]:
        length = len(board)

        sqrt = math.isqrt(length)
        if sqrt * sqrt != length:
            raise ValidationError("Board size must be square of some number")

        for i in range(0, length):
            if 0 > board[i] or board[i] > length:
                raise ValidationError("Board values must be between 0 and board size")

        return board
