import { filter, flatten } from 'ramda';

export interface IPathCoords {
  right: number;
  left: number;
  down: number;
  up: number;
}

const mapCount = (right: number, down: number) => Math.ceil(down / right) + 4; // 4 is buffer, could get fancy with wide results

const processRows = (rows: string[][], numOfMaps: number): string[][] =>
  rows.map((r) => r[0].repeat(numOfMaps).split(''));

const printMap = (map: string[][]): string =>
  map.map((r) => r.join('')).join('\n');

const numberOfTrees = (map: string[][]): number =>
  flatten(map.map((r) => filter((col) => col === 'X', r))).length;

const traverse = (map: string[][], path: Partial<IPathCoords>): string[][] => {
  const retMap = [...map];
  let [curRow, curCol] = [0, 0];
  if (path.right && path.down) {
    while (curRow <= retMap.length) {
      curRow = curRow + path.down;
      curCol = curCol + path.right;
      const row = retMap[curRow];
      if (row) {
        const val = row[curCol];
        if (val === '.') {
          retMap[curRow][curCol] = 'O';
        } else if (val === '#') {
          retMap[curRow][curCol] = 'X';
        } else {
          // console.log(
          //   `reached the end: curRow: ${curRow}, curCol: ${curCol}, rowCount: ${map.length}, colCount: ${map[0].length}`
          // );
          break;
        }
      } else {
        // console.log(
        //   `reached the end: curRow: ${curRow}, curCol: ${curCol}, rowCount: ${map.length}, colCount: ${map[0].length}`
        // );
        break;
      }
    }
  }
  return retMap;
  // for (const [dir, value] of Object.entries(path)) {
  //   console.log('🚀 ~ file: challenge.ts ~ line 12 ~ traverse ~ dir', dir);
  // }
};

export { processRows, traverse, printMap, mapCount, numberOfTrees };
