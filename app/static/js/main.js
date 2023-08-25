async function solveButtonClick() {
    hideMessages();
    clearCellsHighlight();
    clearOutputBoard();

    setProcessing(true);
    var validation_resp = await validateSudoku(getInputBoard());

    if (!validation_resp.isRequestSuccess) {
        onServerError();
        return;
    }

    if (!validation_resp.isValid) {
        showErrorMessage("Sudoku is invalid!");
        highlightInputCells(validation_resp.invalid_cells, "red");
        setProcessing(false);
        return;
    }

    var solve_resp = await solveSudoku(getInputBoard());

    if (!solve_resp.isRequestSuccess) {
        onServerError();
        return;
    }

    if (!solve_resp.isSolved) {
        showErrorMessage("Sudoku is unsolvable!");
    } else {
        showSuccessMessage(`Sudoku solved in ${solve_resp.steps} steps`)
        setOutputBoard(solve_resp.board);
    }

    setProcessing(false);
}

async function generateButtonClick(empty_cells_percent) {
    var resp = await generateSudoku(getBoardSize(), empty_cells_percent);
    hideMessages();

    if (!resp.isRequestSuccess) {
        onServerError();
        return;
    }

    clearBoards();
    setInputBoard(resp.board);
}

function onServerError() {
    hideMessages();
    showErrorMessage("Error during a request to the server");
    setProcessing(false);
}

function hideMessages() {
    var errorElem = document.querySelector('p[id="error-message"]');
    var successElem = document.querySelector('p[id="success-message"]');

    errorElem.style.display = "none"
    successElem.style.display = "none"
}

function showErrorMessage(msg) {
    var elem = document.querySelector('p[id="error-message"]');
    elem.style.display = "block"
    elem.innerHTML = msg;
}

function showSuccessMessage(msg) {
    var elem = document.querySelector('p[id="success-message"]');
    elem.style.display = "block"
    elem.innerHTML = msg;
}

function clearCellsHighlight() {
    for (let i = 0; i < getBoardCellsNum(); i++) {
        highlightInputCell(i, "");
    }
}

function highlightInputCells(cells, color) {
    for (let i = 0; i < cells.length; i++) {
        highlightInputCell(cells[i], color);
    }
}

function highlightInputCell(num, color) {
    var cell = document.querySelector(`input[name=input-${num}]`);
    cell.style.background = color;
}

function clearBoards() {
    clearInputBoard();
    clearOutputBoard();
}

function clearInputBoard() {
    clearCellsHighlight();
    hideMessages();
    for (let i = 0; i < getBoardCellsNum(); i++) {
        setInputCell(i, "");
    }
}

function clearOutputBoard() {
    for (let i = 0; i < getBoardCellsNum(); i++) {
        setOutputCell(i, "");
    }
}

function setInputBoard(board) {
    for (let i = 0; i < board.length; i++) {
        if (board[i] == 0) {
            continue;
        }

        setInputCell(i, board[i]);
    }
}

function setOutputBoard(board) {
    for (let i = 0; i < board.length; i++) {
        if (board[i] == 0) {
            continue;
        }

        setOutputCell(i, board[i]);
    }
}

function setInputCell(num, value) {
    document.querySelector(`input[name=input-${num}]`).value = value;
}

function setOutputCell(num, value) {
    document.querySelector(`input[name=output-${num}]`).value = value;
}

function getInputBoard() {
    var board = []

    for (let i = 0; i < getBoardCellsNum(); i++) {
        board.push(getInputCell(i));
    }

    return board;
}

function getInputCell(num) {
    var val = Number(document.querySelector(`input[name=input-${num}]`).value);
    return val;
}

function getBoardCellsNum() {
    return getBoardSize() * getBoardSize();
}

function getBoardSize() {
    return Number(document.querySelector(".sudoku-board").getAttribute("data-board-size"));
}

function validateCellInput(object) {
    var curVal = object.value;
    var lastChar = curVal[curVal.length - 1];
    var boardSize = document.querySelector(".sudoku-board").getAttribute("data-board-size");

    if (lastChar < '1' && !(lastChar == '0' && curVal.length > 1) || lastChar > '9' || Number(curVal) > Number(boardSize)) {
        object.value = object.value.slice(0, curVal.length - 1);
    }
    else {
        object.oldValue = object.value;
    }

    object.value = object.valueAsNumber;
}

function setProcessing(isProcessing) {
    var solveButton = document.getElementById("solve-button");
    var processingButton = document.getElementById("solve-button-processing");

    if (isProcessing) {
        solveButton.style = "display: none;"
        processingButton.style = "";
    } else {
        solveButton.style = ""
        processingButton.style = "display: none;";
    }
}