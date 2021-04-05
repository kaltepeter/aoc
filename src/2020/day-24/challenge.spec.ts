import { sample, inputs } from './inputs';
import {
  calcNextGeneration,
  coord,
  Direction,
  flipTiles,
  flipTilesConwayStyle,
  getBlackTiles,
  getNeighborCount,
  getPermutationsOfCoords,
  moveTile,
  TileColor,
  TileState,
} from './challenge';

describe(`Day 24: Lobby Layout`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(20);
    expect(sample[0].length).toBe(20);
    expect(sample[0][0]).toBe('se');
    expect(sample[0][sample[0].length - 1]).toBe('sw');
  });

  it(`should handle directions`, () => {
    const [x, y, z] = Direction.w;
    expect(x).toBe(-1);
    expect(y).toBe(1);
    expect(z).toBe(0);
  });
  it(`should move position`, () => {
    expect(moveTile([0, 0, 0], 'nw')).toEqual([0, 1, -1]);
  });

  it(`should flip tiles`, () => {
    const result = flipTiles(sample);
    expect(result.get('0,-2,2')).toBe(TileColor.BLACK);
  });

  it(`should count black tiles for sample`, () => {
    const list = flipTiles(sample);
    const result = [...list.values()].filter((v) => v === TileColor.BLACK);
    expect(result.length).toBe(10);
  });

  it(`should count black tiles`, () => {
    const list = flipTiles(inputs);
    const result = [...list.values()].filter((v) => v === TileColor.BLACK);
    expect(result.length).toBe(523);
  });

  describe(`part II`, () => {
    it(`should return list of black tiles`, () => {
      const testData = new Map<string, number>([
        ['0,0,0', 0b0],
        ['-1,0,0', 0b1],
        ['0,1,0', 0b1],
        ['0,2,0', 0b1],
      ]);
      const result = getBlackTiles(testData);
      expect(result.length).toBe(3);
      expect(result[0].length).toBe(2);
    });

    it(`should return correct number of black tile neighbors`, () => {
      expect(getNeighborCount(0b11110)).toBe(4);
      expect(getNeighborCount(0b11111)).toBe(4);
      expect(getNeighborCount(0b1)).toBe(0);
      expect(getNeighborCount(1)).toBe(0);
      expect(getNeighborCount(0)).toBe(0);
    });

    it(`should calculate the six neighbors`, () => {
      expect(getPermutationsOfCoords([-3, 1, 2]).length).toBe(6);
    });

    it(`should run flipTilesConwayStyle(sample)`, () => {
      const list = flipTiles(sample);

      const res = flipTilesConwayStyle(list, 100);
      const result = getBlackTiles(res);
      expect(result.length).toBe(2208);
    });

    it(`should run flipTilesConwayStyle(input)`, () => {
      const list = flipTiles(inputs);

      const res = flipTilesConwayStyle(list, 100);
      const result = getBlackTiles(res);
      expect(result.length).toBe(4225);
    });
  });
});
