import { calcResult, findRoughness } from './challenge';
import { TileImage } from './tile-image';
import { inputs, sample } from './inputs';
import { Tile } from './tile2';

describe(`Day 20: Jurassic Jigsaw`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(9);
    expect(sample[0][0]).toBe('2311');
    expect(sample[0][1].split('\n')[0]).toBe('..##.#..#.');
  });

  it(`calcResult('1951', '3079', '2971', '1171')`, () => {
    expect(calcResult(['1951', '3079', '2971', '1171'])).toBe(20899048083289);
  });

  it(`calcResult for inputs`, () => {
    const tiles = inputs.map((t) => new Tile(t[0], t[1].split('\n')));
    const image = new TileImage(tiles);
    const corners = image.corners();
    expect(calcResult(corners)).toBe(17250897231301);
  });

  describe(`part II`, () => {
    it(`findMonsters(sample)`, () => {
      const tiles = sample.map((t) => new Tile(t[0], t[1].split('\n')));
      expect(findRoughness(tiles)).toBe(273);
    });

    it(`findMonsters(inputs)`, () => {
      const tiles = inputs.map((t) => new Tile(t[0], t[1].split('\n')));
      expect(findRoughness(tiles)).toBeLessThan(1606);
      expect(findRoughness(tiles)).toBe(1576);
    });
  });
});
