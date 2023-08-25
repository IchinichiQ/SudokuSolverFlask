import math

from flask import Flask, render_template, request, jsonify
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range

from sudoku.BoardValidator import BoardValidator
from sudoku.SudokuBoard import SudokuBoard
from sudoku.SudokuGenerator import SudokuGenerator
from sudoku.SudokuSolver import SudokuSolver

app = Flask(__name__)


class GenerateSchema(Schema):
    size = fields.Integer(strict=True, required=True)
    empty_cells_percent = fields.Float(validate=[Range(min=0.0, max=1.0, error="Value must be between 0.0 and 1.0")],
                                       required=True)


class SolveSchema(Schema):
    board = fields.List(
        fields.Integer(strict=True, required=True),
        validate=BoardValidator(),
        required=True)


class ValidateSchema(Schema):
    board = fields.List(
        fields.Integer(strict=True, required=True),
        validate=BoardValidator(),
        required=True)


@app.route("/", methods=['post', 'get'])
def main():
    selected_board_size = 9
    selected_board_box_size = 3

    if request.method == "POST":
        selected_board_size = int(request.form["selected-board-size"])
        selected_board_box_size = SudokuBoard.box_size_from_board_size(selected_board_size)

    return render_template("main.html", selected_board_size=selected_board_size,
                           selected_board_box_size=selected_board_box_size)


@app.route("/api/v1.0/generate", methods=['post'])
def handler_generate():
    try:
        content = request.get_json()

        try:
            schema = GenerateSchema()
            schema.load(content)
        except ValidationError as err:
            return jsonify(err.messages), 400

        size = content["size"]
        empty_cells_percent = content["empty_cells_percent"]
        board = SudokuGenerator.generate_random_sudoku(size, empty_cells_percent)

        return jsonify({"board": board.to_array()})
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/v1.0/solve", methods=['post'])
def handler_solve():
    try:
        content = request.get_json()

        try:
            schema = SolveSchema()
            schema.load(content)
        except ValidationError as err:
            return jsonify(err.messages), 400

        board_arr = content["board"]
        size = math.isqrt(len(board_arr))

        board = SudokuBoard.from_array(size, board_arr)

        is_solved, steps = SudokuSolver.solve(board)

        resp = {"isSolved": is_solved}
        if is_solved:
            resp["steps"] = steps
            resp["board"] = board.to_array()

        return jsonify(resp)
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/v1.0/validate", methods=['post'])
def handler_validate():
    try:
        content = request.get_json()

        try:
            schema = ValidateSchema()
            schema.load(content)
        except ValidationError as err:
            return jsonify(err.messages), 400

        board_arr = content["board"]
        size = math.isqrt(len(board_arr))

        board = SudokuBoard.from_array(size, board_arr)

        invalid_cells = board.get_invalid_cells()

        resp = {"isValid": len(invalid_cells) == 0}
        if len(invalid_cells) > 0:
            resp["invalid_cells"] = invalid_cells

        return jsonify(resp)
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500
