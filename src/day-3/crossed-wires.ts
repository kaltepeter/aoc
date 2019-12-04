import { from, Observable, of, range } from 'rxjs';
import {
  buffer,
  bufferCount,
  combineAll,
  concatAll,
  flatMap,
  map,
  mergeAll,
  tap,
  toArray,
  withLatestFrom
} from 'rxjs/operators';

const testData = ['U7', 'R6', 'D4', 'L4'];

// tslint:disable-next-line: interface-name
export interface MatrixMetrics {
  maxMovement: number;
  buffer: number;
  rowSize: number;
  gridSize: number;
  startRowIndex: number;
  startColIndex: number;
}

// max places to move in matrix
const getMaxMovement = (d: string[]): number =>
  Math.max(...d.map(p => +p.slice(1)));

let mm: MatrixMetrics;

const setupMatrix = (d: string[]) => {
  const max = getMaxMovement([...d]);
  // buffer for display purposes, round the grid
  const bufferSize = 1;
  // rowsize = max + 1 for home item + (left buffer + right buffer)
  const rowSize = max + 1 + bufferSize * 2;
  const gridSize = rowSize * rowSize;

  // starting position
  const [sRowIndex, sColIndex] = [
    max + bufferSize, // zero base, shift to bottom left in respect to buffer
    bufferSize
  ];

  const metrics: MatrixMetrics = {
    maxMovement: max,
    buffer: bufferSize,
    rowSize,
    gridSize,
    startRowIndex: sRowIndex,
    startColIndex: sColIndex
  };
  return metrics;
};

const commands: any = {
  U: (v: number): number => v,
  D: (v: number): number => -v,
  R: (v: number): number => v,
  L: (v: number): number => -v
};

mm = setupMatrix([...testData]);

const maxMovement = mm.maxMovement;
const matrixBuffer = mm.buffer;
const startRowIndex = mm.startRowIndex;
const startColIndex = mm.startColIndex;

// rows of columns (x col, y row)
let matrix: string[][] = [];

const matrix$ = (m: MatrixMetrics) =>
  range(0, m.gridSize).pipe(
    bufferCount(m.rowSize),
    map(v => new Array(m.rowSize).fill('.')),
    toArray(),
    mergeAll(),
    toArray(),
    map(v => {
      const startRow = [...v[m.startRowIndex]];
      startRow.splice(m.startColIndex, 1, 'o');
      v[m.startRowIndex] = [...startRow];
      return v;
    }),
    tap(finalM => {
      matrix = [...finalM];
    })
  );

const drawRow = (r: string[], v: number, char: string) => {
  for (let i = 0; i < v; i++) {
    r.splice(startColIndex + 1 + i, 1, char);
  }
};

const drawCol = (data: string[], val: number, char: string) => {
  for (let i = 0; i < val; i++) {
    data.splice(startColIndex + 1 + i, 1, char);
  }
};

// testData.map(([commandCode, v]) => {
//   const commandValue = +v;
//   const command = commands[commandCode];
//   const val = command(commandValue);
//   const row = result[startX];
//   const col = result[startX][startY];

//   switch (commandCode) {
//     case 'U':
//       drawCol(row, commandValue, '-');
//       break;
//     case 'R':
//       drawRow(row, commandValue, '-');
//       break;
//     case 'D':
//       break;
//     case 'L':
//       break;
//   }
// });

const drawWires$ = of(testData).pipe(
  withLatestFrom(matrix$(mm)),
  map(([ds, m]) => {
    console.log(ds);
    const retM = [...m];
    const comms: Array<[string, number]> = ds.map(c => [c[0], +c[1]]);
    const updateRow = [...retM[startRowIndex]];
    let [rowCursor, colCursor] = [startRowIndex, startColIndex];

    for (let i = rowCursor - 1; i >= rowCursor - comms[0][1]; i--) {
      const row = [...retM[i]];
      row[colCursor] = i === rowCursor - comms[0][1] ? '+' : '|';
      retM.splice(i, 1, row);
    }
    rowCursor -= comms[0][1];

    // todo: pass in start row
    for (let i = colCursor + 1; i <= comms[1][1] + colCursor; i++) {
      // updateRow[startY + i] = '-';
      const row = [...retM[rowCursor]];
      row[i] = i === comms[1][1] + colCursor ? '+' : '-';
      retM.splice(rowCursor, 1, row);
    }
    colCursor += comms[1][1];

    for (let i = rowCursor + 1; i <= rowCursor + comms[2][1]; i++) {
      const row = [...retM[i]];
      row[colCursor] = i === rowCursor + comms[2][1] ? '+' : '|';
      retM.splice(i, 1, row);
    }

    rowCursor += comms[2][1];

    for (let i = colCursor - 1; i >= colCursor - comms[3][1]; i--) {
      const row = [...retM[rowCursor]];
      row[i] = i === comms[3][1] - colCursor ? '+' : '-';
      retM.splice(rowCursor, 1, row);
    }
    colCursor -= comms[3][1];

    return [retM, m];
  }),
  tap(([d, source]) => {
    printMatrix(d, 'draw');
    printMatrix(source, 'draws');
  })
  // flatMap((command: string) => command),
  // map(c => [c[0], +c[1]]),
  // // map(([c, v]) => {
  // //   return range(0, +v).pipe(map(iv => v));
  // // }),
  // flatMap(v => v),
  // toArray(),
  // tap(console.log)
);

const printFn = (str: string) => {
  const isJest = !!process.env['JEST_WORKER_ID'];
  if (isJest) {
    return;
  }
  console.log(str);
};

const printMatrix = (m: string[][], t: string = ' ', print = printFn) => {
  const title = t.length % 2 === 0 ? t : t + '';
  // max + buffer + spaces for join
  const paddLength =
    maxMovement + matrixBuffer + (maxMovement + matrixBuffer - 1);
  // title length minus space on each side
  const titleL = title.length + 2;
  const halfPad = Math.floor((paddLength - titleL) / 2);
  const padding = new Array(halfPad).fill('-').join('');
  const titleStr: string = [''.padStart(halfPad, '-'), '', title, ''].join(' ');
  print(`${titleStr.padEnd(paddLength, '-')}`);
  m.map((i: string[]) => {
    print(i.join(' '));
  });
  print('');
};

const checkCrossedWires = () => {
  // matrix$.subscribe(d => {
  // printMatrix(d, 'matrix$');
  // printMatrix(matrix, 'matrix');
  // });

  drawWires$.subscribe(d => {});
};
export {
  checkCrossedWires,
  matrix$,
  printMatrix,
  getMaxMovement,
  setupMatrix,
  drawWires$
};
