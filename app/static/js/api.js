const api = new RestClient("api/v1.0").withRes({
    generate: 'generate',
    solve: 'solve',
    validate: 'validate',
})

async function generateSudoku(size, empty_cells_percent) {
    var resp = {};

    try {
        resp = await api.generate.post({ size: size, empty_cells_percent: empty_cells_percent });
        resp.isRequestSuccess = true;
    } catch (err) {
        resp.isRequestSuccess = false;
    }

    return resp;
}

async function validateSudoku(board) {
    var resp = {};

    try {
        resp = await api.validate.post({ board: board });
        resp.isRequestSuccess = true;
    } catch (err) {
        resp.isRequestSuccess = false;
    }

    return resp;
}

async function solveSudoku(board) {
    var resp = {};

    try {
        resp = await api.solve.post({ board: board });
        resp.isRequestSuccess = true;
    } catch (err) {
        resp.isRequestSuccess = false;
    }

    return resp;
}