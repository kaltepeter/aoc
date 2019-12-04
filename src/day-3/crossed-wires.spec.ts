import {
  drawWires$,
  getMaxMovement,
  matrix$,
  MatrixMetrics,
  printMatrix,
  setupMatrix
} from './crossed-wires';

const wireTestData = [
  ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
  ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'],
  ['U7', 'R6', 'D4', 'L4']
];

const expectedWire3 = `
. . . . . . . . . .
. + - - - - - + . .
. | . . . . . | . .
. | . . . . . | . .
. | . . . . . | . .
. | . - - - - + . .
. | . . . . . . . .
. | . . . . . . . .
. o . . . . . . . .
. . . . . . . . . .
`.trim();

const expectedMatrix3 = [
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', 'o', '.', '.', '.', '.', '.', '.', '.', '.'],
  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
];

describe('3: crossed wires', () => {
  let expectedMetrics: MatrixMetrics;
  let metrics: MatrixMetrics;

  beforeEach(() => {
    expectedMetrics = {
      maxMovement: 83,
      buffer: 1,
      rowSize: 86,
      gridSize: 7396,
      startRowIndex: 84,
      startColIndex: 1
    };
    metrics = {
      maxMovement: 83,
      buffer: 1,
      rowSize: 86,
      gridSize: 7396,
      startRowIndex: 84,
      startColIndex: 1
    };
  });

  test('calc maxMovement', () => {
    const testData = [...wireTestData[0]];
    expect(getMaxMovement(testData)).toBe(83);
  });

  test('get matrixMetrics', () => {
    // console.log(metrics);
    const m = setupMatrix([...wireTestData[0]]);
    expect(m).toEqual(expectedMetrics);
  });

  test('creates matrix with buffer', async () => {
    expect.assertions(3);
    const row = new Array(metrics.rowSize).fill('.');
    const homeRow = [...row];
    homeRow.splice(1, 1, 'o');
    const val$ = await matrix$(metrics).toPromise();
    expect(val$.length).toBe(86);
    expect(val$[0]).toEqual(row);
    expect(val$[84]).toEqual(homeRow);
  });

  test('draws wire on matrix', async () => {
    expect.assertions(2);
    const expectedOut = expectedWire3.split('\n').map(r => r.split(' '));
    const val$ = await drawWires$.toPromise();
    expect(val$[0]).toEqual(expectedOut);
    expect(val$[1]).toEqual(expectedMatrix3);
  });

  test('printMatrix', () => {
    expect.assertions(5);
    const printerFn = jest.fn();
    printMatrix(expectedMatrix3, 'matrix', printerFn);
    expect(printerFn).toHaveBeenCalled();
    expect(printerFn).toHaveBeenCalledTimes(12);
    expect(printerFn).nthCalledWith(1, '---  matrix ---');
    expect(printerFn).nthCalledWith(10, '. o . . . . . . . .');
    expect(printerFn).lastCalledWith('');
  });
});
