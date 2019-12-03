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
const commands: any = {
  U: (v: number): number => v,
  D: (v: number): number => -v,
  R: (v: number): number => v,
  L: (v: number): number => -v
};
const max = Math.max(...testData.map(p => +p[1]));
const matrixBuffer = 2;
const [startX, startY] = [max - matrixBuffer / 2, matrixBuffer / 2];
const initialRow = new Array(max + matrixBuffer).fill('.');

let matrix: string[][] = [];

const matrix$ = range(0, (max + matrixBuffer) * (max + matrixBuffer)).pipe(
  bufferCount(max + matrixBuffer),
  map(v => initialRow),
  toArray(),
  mergeAll(),
  toArray(),
  map(v => {
    const startRow = [...v[startX]];
    const newRow = [
      ...startRow.slice(0, startY),
      'o',
      ...startRow.slice(startY + 1)
    ];
    v[startX] = [...newRow];
    return v;
  }),
  tap(m => {
    matrix = [...m];
  })
);

// const row = result[startX];
// const newRow = row.splice(startY, 1, 'O');

const drawRow = (r: string[], v: number, char: string) => {
  for (let i = 0; i < v; i++) {
    r.splice(startY + 1 + i, 1, char);
  }
};

const drawCol = (data: string[], val: number, char: string) => {
  for (let i = 0; i < val; i++) {
    data.splice(startY + 1 + i, 1, char);
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
  withLatestFrom(matrix$),
  map(([ds, m]) => ds),
  tap(console.log),
  flatMap((command: string) => command),
  map(c => [c[0], +c[1]]),
  // map(([c, v]) => {
  //   return range(0, +v).pipe(map(iv => v));
  // }),
  flatMap(v => v),
  toArray(),
  tap(console.log)
);

const printMatrix = (m: string[][], t: string = ' ') => {
  const title = t.length % 2 === 0 ? t : t + '';
  // max + buffer + spaces for join
  const paddLength = max + matrixBuffer + (max + matrixBuffer - 1);
  // title length minus space on each side
  const titleL = title.length + 2;
  const halfPad = Math.floor((paddLength - titleL) / 2);
  const padding = new Array(halfPad).fill('-').join('');
  const titleStr: string = [''.padStart(halfPad, '-'), '', title, ''].join(' ');
  console.log(`${titleStr.padEnd(paddLength, '-')}`);
  m.map((i: string[]) => {
    console.log(i.join(' '));
  });
  console.log('');
};

const checkCrossedWires = () => {
  matrix$.subscribe(d => {
    printMatrix(d, 'matrix$');
    printMatrix(matrix, 'matrix');
  });
};
export { checkCrossedWires };
