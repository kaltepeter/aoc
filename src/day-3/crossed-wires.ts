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

// tslint:disable-next-line: interface-name
export interface DrawResult {
  rowCursor: number;
  colCursor: number;
  m: string[][];
  prevM: string[][];
}

type DrawFn = (
  dist: number,
  r: number,
  c: number,
  curM: string[][]
) => DrawResult;

// tslint:disable-next-line: interface-name

// max places to move in matrix
const getMaxMovement = (d: string[]): number =>
  Math.max(...d.map(p => +p.slice(1)));

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

const drawPath: any = {
  U: (v: number): number => v,
  D: (v: number): number => -v,
  R: (v: number): number => v,
  L: (v: number): number => -v
};

// mm = setupMatrix([...testData]);

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

const drawU: DrawFn = (dist, r, c, curM) => {
  const newM = [...curM];
  const total = r - dist;
  for (let i = r - 1; i >= total; i--) {
    const row = [...newM[i]];
    row[c] = i === total ? '+' : '|';
    newM.splice(i, 1, row);
  }
  r -= dist;
  return {
    rowCursor: r,
    colCursor: c,
    m: newM,
    prevM: curM
  };
};

const drawD: DrawFn = (dist, r, c, curM) => {
  const newM = [...curM];
  const total = r + dist;
  for (let i = r + 1; i <= total; i++) {
    const row = [...newM[i]];
    row[c] = i === total ? '+' : '|';
    newM.splice(i, 1, row);
  }
  r += dist;
  return {
    rowCursor: r,
    colCursor: c,
    m: newM,
    prevM: curM
  };
};

const drawR: DrawFn = (dist, r, c, curM) => {
  const newM = [...curM];
  const total = dist + c;
  // todo: pass in start row
  for (let i = c + 1; i <= total; i++) {
    const row = [...newM[r]];
    row[i] = i === total ? '+' : '-';
    newM.splice(r, 1, row);
  }
  c += dist;
  return {
    rowCursor: r,
    colCursor: c,
    m: newM,
    prevM: curM
  };
};

const drawL: DrawFn = (dist, r, c, curM) => {
  const newM = [...curM];
  const total = c - dist;

  for (let i = c - 1; i >= total; i--) {
    const row = [...newM[r]];
    row[i] = i === total ? '+' : '-';
    newM.splice(r, 1, row);
  }

  c -= dist;
  return {
    rowCursor: r,
    colCursor: c,
    m: newM,
    prevM: curM
  };
};

const drawWires$ = (instructions: string[], matrixMetrics: MatrixMetrics) =>
  of(instructions).pipe(
    withLatestFrom(matrix$(matrixMetrics)),
    map(([ds, m]) => {
      let retM = [...m];
      const paths: Array<[string, number]> = ds.map(c => [c[0], +c[1]]);
      const updateRow = [...retM[matrixMetrics.startRowIndex]];
      let [rowCursor, colCursor] = [
        matrixMetrics.startRowIndex,
        matrixMetrics.startColIndex
      ];

      paths.map(p => {
        const [command, distance] = p;
        console.log(`path: ${command} ${distance}`);
      });

      const u = drawU(paths[0][1], rowCursor, colCursor, retM);
      rowCursor = u.rowCursor;
      retM = u.m;

      const r = drawR(paths[1][1], rowCursor, colCursor, retM);
      colCursor = r.colCursor;
      retM = r.m;

      const d = drawD(paths[2][1], rowCursor, colCursor, retM);
      rowCursor = d.rowCursor;
      retM = d.m;

      const l = drawL(paths[3][1], rowCursor, colCursor, retM);
      colCursor = l.colCursor;
      retM = l.m;

      return [retM, m];
    }),
    tap(([d, source]) => {
      printMatrix(d, 'draw', matrixMetrics);
      printMatrix(source, 'draws', matrixMetrics);
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

const printMatrix = (
  m: string[][],
  t: string = ' ',
  mm: MatrixMetrics,
  print = printFn
) => {
  const title = t.length % 2 === 0 ? t : t + '';
  // max + buffer + spaces for join
  const paddLength =
    mm.maxMovement + mm.buffer + (mm.maxMovement + mm.buffer - 1);
  // title length minus space on each side
  const titleL = title.length + 2;
  const halfPad = Math.floor((paddLength - titleL) / 2);
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

  drawWires$([...testData], setupMatrix([...testData])).subscribe(d => {});
};
export {
  checkCrossedWires,
  matrix$,
  printMatrix,
  getMaxMovement,
  setupMatrix,
  drawWires$
};
