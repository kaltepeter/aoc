import { mapCount, numberOfTrees, processRows, traverse } from './challenge';
import { inputs } from './inputs';

describe('3: toboggan path', () => {
  test(`returns 7`, () => {
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
    const numOfMaps = mapCount(3, values.length);
    const mapVals = processRows(values, numOfMaps);
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
});
