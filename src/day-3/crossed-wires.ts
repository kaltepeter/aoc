import { from, merge, Observable, of, range } from 'rxjs';
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
  withLatestFrom,
  zip
} from 'rxjs/operators';

// const testData = ['U7', 'R6', 'D4', 'L4'];
const testData = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'];

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
  // console.log(metrics);
  return metrics;
};
// rows of columns (x col, y row)
let matrix: string[][] = [];

const matrix$ = (m: MatrixMetrics) =>
  range(0, m.gridSize).pipe(
    bufferCount(m.rowSize),
    map(v => new Array(m.rowSize).fill('.')),
    toArray(),
    mergeAll(),
    toArray(),
    // map(v => {
    //   const startRow = [...v[m.startRowIndex]];
    //   startRow.splice(m.startColIndex, 1, 'o');
    //   v[m.startRowIndex] = [...startRow];
    //   return v;
    // }),
    tap(finalM => {
      matrix = [...finalM];
    })
  );

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

const execCommand = (commandCode: string, ...args: Parameters<DrawFn>) => {
  let drawResult: DrawResult;
  switch (commandCode) {
    case 'U':
      drawResult = drawU(...args);
      break;
    case 'R':
      drawResult = drawR(...args);
      break;
    case 'D':
      drawResult = drawD(...args);
      break;
    case 'L':
      drawResult = drawL(...args);
      break;
    default:
      drawResult = {
        rowCursor: args[1],
        colCursor: args[2],
        m: args[3],
        prevM: args[3]
      };
      break;
  }
  return drawResult;
};

const calcDirections = (paths: Array<[string, number]>, m: MatrixMetrics) => {
  const topIndex = paths.findIndex(path => path[0].match('U'));
  const bottomIndex = paths.findIndex(path => path[0].match('D'));
  const rightIndex = paths.findIndex(path => path[0].match('R'));
  const leftIndex = paths.findIndex(path => path[0].match('L'));
  const getVal = (pi: number) => (paths[pi] ? paths[pi][1] : 0);
  // const calcDir = ()
  return {
    top: getVal(topIndex),
    right: getVal(rightIndex),
    bottom: getVal(bottomIndex),
    left: getVal(leftIndex),
    startX:
      getVal(rightIndex) < getVal(leftIndex) ? m.buffer : m.rowSize - m.buffer,
    startY:
      getVal(bottomIndex) < getVal(topIndex) ? m.buffer : m.rowSize - m.buffer
  };
};

const drawWires$ = (instructions: string[], matrixMetrics: MatrixMetrics) =>
  of(instructions).pipe(
    map(c => c.map(val => [val[0], +val.slice(1)])),
    withLatestFrom(matrix$(matrixMetrics)),
    map(([ds, m]) => {
      console.log(matrixMetrics, ds);
      const v = [...m];
      const startRow = [...v[matrixMetrics.startRowIndex]];
      startRow.splice(matrixMetrics.startColIndex, 1, 'o');
      v[matrixMetrics.startRowIndex] = [...startRow];
      return v;
    }),
    // tap(console.log),
    map(m => {
      // console.log(instructions);
      let retM = [...m];
      const paths: Array<[string, number]> = instructions.map((c: string) => [
        c[0],
        +c.slice(1)
      ]);
      // const firstMoveByDirection = calcDirections(paths, matrixMetrics);
      // console.log(firstMoveByDirection);
      // const updateRow = [...retM[matrixMetrics.startRowIndex]];
      let [rowCursor, colCursor] = [
        matrixMetrics.startRowIndex,
        matrixMetrics.startColIndex
      ];

      paths.map(p => {
        const [command, distance] = p;
        console.log(`path: ${command} ${distance}`);
        const commandResult = execCommand(
          command,
          distance,
          rowCursor,
          colCursor,
          retM
        );
        rowCursor = commandResult.rowCursor;
        colCursor = commandResult.colCursor;
        retM = commandResult.m;
      });

      return [retM, m];
    }),
    tap(([d, source]) => {
      printMatrix(d, 'draw', matrixMetrics);
      printMatrix(source, 'draws', matrixMetrics);
    })
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
  drawWires$,
  calcDirections
};
