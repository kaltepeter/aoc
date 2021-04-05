import { mapCount, numberOfTrees, processRows, traverse } from './challenge';
import { inputs } from './inputs';

const values = [
  ['..##.......'],
  ['#...#...#..'],
  ['.#....#..#.'],
  ['..#.#...#.#'],
  ['.#...##..#.'],
  ['..#.##.....'],
  ['.#.#.#....#'],
  ['.#........#'],
  ['#.##...#...'],
  ['#...##....#'],
  ['.#..#...#.#'],
];

describe('3: toboggan path', () => {
  test(`returns 7`, () => {
    const numOfMaps = mapCount(3, values.length);
    const mapVals = processRows([...values], numOfMaps);
    const res = traverse(mapVals, { right: 3, down: 1 });

    expect(numberOfTrees(res)).toBe(7);
  });

  test(`value of sample data numberOfTrees()`, () => {
    const data = [...inputs];
    const numOfMaps = mapCount(3, data.length);
    const mapVals = processRows(data, numOfMaps);
    const res = traverse(mapVals, { right: 3, down: 1 });
    expect(numberOfTrees(res)).toBe(299);
  });

  describe('part II', () => {
    describe.each([
      [{ right: 1, down: 1 }, 2],
      [{ right: 3, down: 1 }, 7],
      [{ right: 5, down: 1 }, 3],
      [{ right: 7, down: 1 }, 4],
      [{ right: 1, down: 2 }, 2],
    ])('traverse(mapVals, %o)', (value, expected) => {
      test(`returns ${expected}`, () => {
        const numOfMaps = mapCount(3, values.length);
        const mapVals = processRows([...values], numOfMaps);
        const res = traverse(mapVals, value);
        expect(numberOfTrees(res)).toBe(expected);
        expect([2, 7, 3, 4, 2].reduce((acc, c) => (acc *= c), 1)).toBe(336);
      });
    });

    describe.each([
      [{ right: 1, down: 1 }, 67],
      [{ right: 3, down: 1 }, 299],
      [{ right: 5, down: 1 }, 67],
      [{ right: 7, down: 1 }, 71],
      [{ right: 1, down: 2 }, 38],
    ])('traverse(inputs, %o)', (value, expected) => {
      test(`returns ${expected}`, () => {
        const data = [...inputs];
        const numOfMaps = mapCount(3, data.length);
        const mapVals = processRows(data, numOfMaps);
        const res = traverse(mapVals, value);
        expect(numberOfTrees(res)).toBe(expected);
        expect([67, 299, 67, 71, 38].reduce((acc, c) => (acc *= c), 1)).toBe(
          3621285278
        );
      });
    });
  });
});
