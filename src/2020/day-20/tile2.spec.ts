import { EDGE_LABEL, SIDE } from './constants';
import { Tile } from './tile2';

describe(`tile2`, () => {
  let tile: Tile;
  beforeEach(() => {
    const data = ['12', '45'];
    tile = new Tile('1', data);
  });

  it(`allEdges()`, () => {
    expect(tile.allEdges()).toEqual([
      '12',
      '25',
      '45',
      '14',
      '21',
      '52',
      '54',
      '41',
    ]);
  });

  it(`edgeFor`, () => {
    expect(tile.edgeFor(EDGE_LABEL.A)).toEqual('12');
    expect(tile.edgeFor(EDGE_LABEL.B)).toEqual('25');
  });

  describe(`edgeAt`, () => {
    it(`returns the edge at a give position`, () => {
      expect(tile.edgeAt(SIDE.N)).toBe('12');
      expect(tile.edgeAt(SIDE.E)).toBe('25');
      expect(tile.edgeAt(SIDE.S)).toBe('45');
      expect(tile.edgeAt(SIDE.W)).toBe('14');
    });

    it(`works with flip`, () => {
      tile.flip();
      expect(tile.edgeAt(SIDE.N)).toBe('21');
    });

    it(`works with rotate`, () => {
      tile.rotate();
      expect(tile.edgeAt(SIDE.N)).toBe('41');
    });
  });

  describe(`flip`, () => {
    it(`flips the tile on it's y axis`, () => {
      tile.flip();
      expect(tile.edgeAt(SIDE.N)).toBe('21');
      expect(tile.edgeAt(SIDE.E)).toBe('14');
      expect(tile.edgeAt(SIDE.S)).toBe('54');
      expect(tile.edgeAt(SIDE.W)).toBe('25');
    });
    it(`two flips don't modify the tile`, () => {
      tile.flip();
      tile.flip();

      expect(tile.edgeAt(SIDE.N)).toBe('12');
      expect(tile.edgeAt(SIDE.E)).toBe('25');
      expect(tile.edgeAt(SIDE.S)).toBe('45');
      expect(tile.edgeAt(SIDE.W)).toBe('14');
    });
  });

  describe(`rotate`, () => {
    it(`rotates edge positions`, () => {
      tile.rotate();
      expect(tile.edgeAt(SIDE.N)).toBe('41');
    });

    it(`rotate edge positions 3 times`, () => {
      tile.rotate();
      tile.rotate();
      tile.rotate();
      expect(tile.edgeAt(SIDE.W)).toBe('21');
    });
  });

  describe(`hadEdge()`, () => {
    it(`returns true if the requested orientation is possible`, () => {
      expect(tile.hasEdge('25')).toBe(true);
    });
    it(`returns false if the requested orientation is not`, () => {
      expect(tile.hasEdge('XX')).toBe(false);
    });
  });

  describe(`toString()`, () => {
    it(`returns a formatted string with heading`, () => {
      const result = ['12', '45'].join('\n');
      expect(tile.toString()).toBe(result);
    });
    it(`optionally prints a header with the tile id`, () => {
      const result = ['12', '45'].join('\n');
      expect(tile.toString()).toBe(result);
    });
    it(`handles rotate`, () => {
      tile.rotate();
      const result = ['41', '52'].join('\n');
      expect(tile.toString()).toBe(result);
    });
    it(`handles flip`, () => {
      tile.flip();
      const result = ['21', '54'].join('\n');
      expect(tile.toString()).toBe(result);
    });
  });

  describe(`neighborOf`, () => {
    let neighbor: Tile;

    beforeEach(() => {
      neighbor = new Tile('2', ['12', '88']);
    });
    it(`returns true if tiles share a side`, () => {
      expect(tile.neighborOf(neighbor)).toBe(true);
    });
    it(`returns true if the tile is fliped share a side`, () => {
      neighbor.flip();
      expect(tile.neighborOf(neighbor)).toBe(true);
    });
    it(`returns false if tiles don't share a side`, () => {
      const neighbor2 = new Tile('3', ['88', '88']);
      expect(tile.neighborOf(neighbor2)).toBe(false);
    });
    it(`returns false if a tile is compared to itself`, () => {
      expect(tile.neighborOf(tile)).toBe(false);
    });
  });

  describe(`sharedEdges`, () => {
    it(`returns an array of all orientations of shared edges`, () => {
      const neighbor = new Tile('2', ['12', '88']);
      expect(tile.sharedEdges(neighbor)).toEqual(['12', '21']);
    });
    it(`"returns an empty array if there are no shared edges`, () => {
      const neighbor = new Tile('2', ['88', '88']);
      expect(tile.sharedEdges(neighbor)).toEqual([]);
    });
  });

  describe(`arrange()`, () => {
    it(`it rotates tile into the requested orientation`, () => {
      tile.arrange(SIDE.W, '25');
      expect(tile.edgeAt(SIDE.W)).toBe('25');
    });
    it(`it flips tile into the requested orientation`, () => {
      tile.arrange(SIDE.W, '52');
      expect(tile.edgeAt(SIDE.W)).toBe('52');
    });
    it(`returns false if the tile cannot be arranged as requested`, () => {
      expect(tile.arrange(SIDE.W, 'XX')).toBe(false);
    });
  });

  describe(`removeBorders()`, () => {
    it(`returns a borderless tile`, () => {
      const data = ['****', '*..*', '*..*', '****'];
      const newTile = new Tile('3', data);
      expect(newTile.removeBorders()).toEqual(['..', '..']);
    });
  });
});
