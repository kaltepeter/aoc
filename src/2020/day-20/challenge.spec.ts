import { sample, inputs } from './inputs';
import {
  calcResult,
  getCorners,
  getEdgesForTile,
  processTiles,
  Tile,
} from './challenge';

describe(`Day 20: Jurassic Jigsaw`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(9);
    expect(sample[0][0]).toBe('2311');
    expect(sample[0][1].split('\n')[0]).toBe('..##.#..#.');
  });

  it(`getEdgesForTile(sample[0][1])`, () => {
    expect(Array.from(getEdgesForTile(sample[0][1]))).toEqual(
      jasmine.arrayContaining([
        '..##.#..#.',
        '..###..###',
        '.#####..#.',
        '...#.##..#',
        '.#..#.##..',
        '###..###..',
        '.#..#####.',
        '#..##.#...',
      ])
    );
  });

  it(`Tile.sharedEdges()`, () => {
    const tile1 = new Tile(sample[0][1]);
    const tile2 = new Tile(sample[1][1]);
    expect(tile1.sharedEdges(tile2)).toEqual(
      jasmine.arrayContaining(['.#####..#.', '.#####..#.'])
    );
  });

  it(`Tile.neighborOf()`, () => {
    const tile1 = new Tile(sample[0][1]);
    const tile2 = new Tile(sample[1][1]);
    expect(tile1.neighborOf(tile2)).toBe(true);
  });

  it(`processTiles(sample)`, () => {
    expect(processTiles(sample).size).toBe(9);
  });

  it(`getCorners(sample)`, () => {
    const tiles = processTiles(sample);
    expect(getCorners(tiles)).toEqual(
      jasmine.arrayContaining(['1951', '3079', '2971', '1171'])
    );
  });

  it(`calcResult('1951', '3079', '2971', '1171')`, () => {
    expect(calcResult(['1951', '3079', '2971', '1171'])).toBe(20899048083289);
  });

  it(`calcResult for inputs`, () => {
    const tiles = processTiles(inputs);
    const corners = getCorners(tiles);
    expect(calcResult(corners)).toBe(17250897231301);
  });
});
