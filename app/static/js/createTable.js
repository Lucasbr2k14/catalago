function createTable(matrix) {
    const head = matrix[0];
    const body = matrix.slice(1);

    return `
        <table>
            <thead>
                ${createLine(head, true)}
            </thead>
            <tbody>
                ${body.map(line => createLine(line)).join('')}
            </tbody>
        </table>
    `;
}

function createLine(line, isHeader = false) {
    return `
        <tr>
            ${line.map(value => createCell(value, isHeader)).join('')}
        </tr>
    `;
}

function createCell(value, isHeader = false) {
    if (isHeader) {
        return `<th>${value}</th>`;
    }

    return `<td>${value}</td>`;
}

