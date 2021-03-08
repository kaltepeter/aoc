import { sample, inputs } from './inputs';
import { Direction, flipTiles, moveTile, TileColor } from './challenge';

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
});
