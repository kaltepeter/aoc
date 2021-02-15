import { TileImage } from './tile-image';
import { sample } from './inputs';
import { Tile } from './tile2';

describe(`Image`, () => {
  let image: TileImage;
  let t2311: Tile;

  beforeEach(() => {
    const tiles = sample.map((t) => new Tile(t[0], t[1].split('\n')));
    image = new TileImage(tiles);
    t2311 = tiles[0];
  });

  it(`has tiles`, () => {
    expect(image.tiles.length).toBe(9);
  });

  describe(`neighbors`, () => {
    it(`builds an adjacency list of tiles`, () => {
      expect(image.neighbors(t2311.id).map((t) => t.id)).toEqual([
        '1951',
        '1427',
        '3079',
      ]);
    });
  });

  describe(`neighborsOf`, () => {
    it(`returns an array of neighboring tiles`, () => {
      expect(image.neighborsOf(t2311).map((t) => t.id)).toEqual([
        '1951',
        '1427',
        '3079',
      ]);
    });
  });

  it(`corners`, () => {
    const corners = image.corners();
    expect(corners).toEqual(['1951', '1171', '2971', '3079']);
  });

  it(`reassemble`, () => {
    image.reassemble();
    const boardIds = image.assembledImage.map((r) => r.map((t) => t.id));
    expect(boardIds).toEqual([
      ['1951', '2311', '3079'],
      ['2729', '1427', '2473'],
      ['2971', '1489', '1171'],
    ]);
  });
});
