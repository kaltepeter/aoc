import { of, range } from 'rxjs';
import {
  bufferCount,
  map,
  mergeAll,
  tap,
  toArray,
  withLatestFrom,
} from 'rxjs/operators';

const testData = ['U7', 'R6', 'D4', 'L4'];
// const testData = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'];

export type StartMetrics = [number, number];

// tslint:disable-next-line: interface-name
export interface MatrixMetrics {
  maxMovement: number;
  buffer: number;
  rowSize: number;
  colSize: number;
  gridSize: number;
  startRowIndex: number;
  startColIndex: number;
  xMove: number;
  startX: number;
  yMove: number;
  startY: number;
  firstMoves: {
    up: StartMetrics;
    right: StartMetrics;
    down: StartMetrics;
    left: StartMetrics;
  };
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
  Math.max(...d.map((p) => +p.slice(1)));

/**
 * takes commands and converts to array of command, distance
 * @param commands ['D7,'R4','U2','L2']
 * @returns [['D', 7], ['R', 4], ['U', 2], ['L', 2]]
 */
const getPaths = (commands: string[]): [string, number][] =>
  commands.map((val) => [val[0], +val.slice(1)]);

const setupMatrix = (d: string[]): MatrixMetrics => {
  const max = getMaxMovement([...d]);
  // buffer for display purposes, round the grid
  const bufferSize = 1;

  const paths = getPaths(d);
  const firstMoves = calcDirections(paths);

  const getMoveDistance = (dirs: string[]) => {
    const dist = [...paths]
      .filter(([command]) => dirs.includes(command))
      .reduce((acc, [_, distance]) => {
        // start = command === dirs[0] ? start + distance : start - distance;
        acc += distance;
        return acc;
      }, 0);
    return [dist];
  };

  const getStart = (
    first: StartMetrics,
    second: StartMetrics,
    size: number,
    buffer: number
  ) => (first[0] < second[0] ? size - buffer : buffer);

  const [xMove] = getMoveDistance(['L', 'R']);
  const [yMove] = getMoveDistance(['U', 'D']);
  // rowsize = max + 1 for home item + (left buffer + right buffer)
  // const rowSize = max + 1 + bufferSize * 2;
  const rowSize = xMove;
  const colSize = yMove;
  const gridSize = rowSize * colSize;
  const startX = getStart(
    firstMoves.left,
    firstMoves.right,
    colSize,
    bufferSize
  );
  const startY = getStart(firstMoves.up, firstMoves.down, rowSize, bufferSize);

  // starting position
  const [sRowIndex, sColIndex] = [
    max + bufferSize, // zero base, shift to bottom left in respect to buffer
    bufferSize,
  ];

  const metrics = {
    maxMovement: max,
    buffer: bufferSize,
    rowSize,
    colSize,
    gridSize,
    startRowIndex: sRowIndex,
    startColIndex: sColIndex,
    xMove,
    startX,
    yMove,
    startY,
    firstMoves,
  };
  // console.log(metrics);
  return metrics;
};

const matrix$ = (m: MatrixMetrics) =>
  range(0, m.gridSize).pipe(
    bufferCount(m.rowSize),
    map(() => new Array<string>(m.rowSize).fill('.')),
    toArray(),
    mergeAll(),
    toArray()
    // map(v => {
    //   const startRow = [...v[m.startRowIndex]];
    //   startRow.splice(m.startColIndex, 1, 'o');
    //   v[m.startRowIndex] = [...startRow];
    //   return v;
    // }),
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
    prevM: curM,
  };
};
// const drawU: DrawFn = (dist, r, c, curM) => {
//   const newM = [...curM];
//   // const total = r - dist;
//   for (let i = 0; i < dist; i++) {
//     newM.unshift(['|']);
//   }
//   // for (let i = r - 1; i >= total; i--) {
//   //   const row = [...newM[i]];
//   //   row[c] = i === total ? '+' : '|';
//   //   newM.splice(i, 1, row);
//   // }
//   r = 0;
//   // console.log(newM);
//   return {
//     rowCursor: r,
//     colCursor: c,
//     m: newM,
//     prevM: curM
//   };
// };

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
    prevM: curM,
  };
};

// const drawD: DrawFn = (dist, r, c, curM) => {
//   const newM = [...curM];
//   const total = r + dist;
//   const draw = new Array(dist).fill('|');
//   for (let i = 1; i < dist; i++) {
//     console.log('1', newM[r + i], draw, c);
//     newM[r + i].concat(draw);
//   }
//   r = total;
//   return {
//     rowCursor: r,
//     colCursor: c,
//     m: newM,
//     prevM: curM
//   };
// };

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
    prevM: curM,
  };
};

// const drawR: DrawFn = (dist, r, c, curM) => {
//   console.log(curM);
//   const newM = [...curM];
//   const total = dist + c;
//   // todo: pass in start row
//   // for (let i = c + 1; i <= total; i++) {
//   //   const row = [...newM[r]];
//   //   row[i] = i === total ? '+' : '-';
//   //   newM.splice(r, 1, row);
//   // }
//   for (let i = 0; i < dist; i++) {
//     newM[r].push('-');
//   }
//   c = total;
//   console.log(newM);
//   return {
//     rowCursor: r,
//     colCursor: c,
//     m: newM,
//     prevM: curM
//   };
// };

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
    prevM: curM,
  };
};

// const drawL: DrawFn = (dist, r, c, curM) => {
//   const newM = [...curM];
//   const total = c - dist;

//   for (let i = c - 1; i >= total; i--) {
//     // const row = [...newM[r]];
//     // row[i] = i === total ? '+' : '-';
//     // newM.splice(r, 1, row);
//   }

//   c -= dist;
//   return {
//     rowCursor: r,
//     colCursor: c,
//     m: newM,
//     prevM: curM
//   };
// };

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
        prevM: args[3],
      };
      break;
  }
  return drawResult;
};

const calcDirections = (
  paths: [string, number][]
): MatrixMetrics['firstMoves'] => {
  const upIndex = paths.findIndex((path) => path[0].match('U'));
  const downIndex = paths.findIndex((path) => path[0].match('D'));
  const rightIndex = paths.findIndex((path) => path[0].match('R'));
  const leftIndex = paths.findIndex((path) => path[0].match('L'));
  const getVal = (pi: number) => (paths[pi] ? paths[pi][1] : 0);
  return {
    up: [upIndex, getVal(upIndex)],
    right: [rightIndex, getVal(rightIndex)],
    down: [downIndex, getVal(downIndex)],
    left: [leftIndex, getVal(leftIndex)],
  };
};

// const drawWires2$ = (instructions: string[], matrixMetrics: MatrixMetrics) => {
//   const retMatrix: string[][] = [['o']];
//   console.log(matrixMetrics);
//   return of(instructions).pipe(
//     mergeMap((c) => getPaths(c)),
//     reduce(
//       (acc, c) => {
//         const command = c[0];
//         const distance = c[1];
//         console.log('TCL: command, distance', command, distance);
//         const retM = [...acc];
//         let rowCursor = 0;
//         let colCursor = 0;
//         const commandResult = execCommand(
//           command,
//           distance,
//           rowCursor,
//           colCursor,
//           retM
//         );
//         rowCursor = commandResult.rowCursor;
//         colCursor = commandResult.colCursor;
//         acc = commandResult.m;

//         return acc;
//       },
//       [...retMatrix]
//     ),
//     tap((d) => {
//       console.log(d);
//       // console.log(matrixMetrics);
//       printMatrix(d, 'draw', matrixMetrics);
//     }),
//     // tap(console.log),
//     withLatestFrom(matrix$(matrixMetrics))
//     // map(([ds, m]) => {
//     //   // console.log('TCL: ds', ds);
//     // }),
//     // map(d => retMatrix),
//   );
// };

const drawWires$ = (instructions: string[], matrixMetrics: MatrixMetrics) =>
  of(instructions).pipe(
    // map(path => {
    //   console.log(path);
    //   return path;
    // }),
    withLatestFrom(matrix$(matrixMetrics)),
    map(([_, m]) => {
      console.log(matrixMetrics);
      const v = [...m];
      const startRow = [...v[matrixMetrics.startY]];
      startRow.splice(matrixMetrics.startX, 1, 'o');
      v[matrixMetrics.startY] = [...startRow];
      return v;
    }),
    map((m) => {
      console.log(instructions);
      let retM = [...m];
      const paths = getPaths(instructions);
      console.log(matrixMetrics.firstMoves);
      // const updateRow = [...retM[matrixMetrics.startRowIndex]];
      let [rowCursor, colCursor] = [
        matrixMetrics.startRowIndex,
        matrixMetrics.startColIndex,
      ];

      paths.map((p) => {
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
    tap(([d]) => {
      printMatrix(d, 'draw', matrixMetrics);
      // printMatrix(source, 'draws', matrixMetrics);
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

  drawWires$([...testData], setupMatrix([...testData])).subscribe(() => {});
  // drawWires2$([...testData], setupMatrix([...testData])).subscribe(d => {});
};
export {
  calcDirections,
  checkCrossedWires,
  drawWires$,
  getMaxMovement,
  matrix$,
  printMatrix,
  setupMatrix,
};
