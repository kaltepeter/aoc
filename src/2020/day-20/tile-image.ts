import { transpose } from 'ramda';
import { SIDE } from './constants';
import { Tile } from './tile2';

// function notEmpty<TValue>(value: TValue | null | undefined): value is TValue {
//   return value !== null && value !== undefined;
// }

class TileImage {
  dimension = 0;
  assembledImage: Tile[][] = [];
  seen = new Set<string>();
  private _corners: string[] = [];
  private _neighbors = new Map<string, Tile[]>();

  constructor(readonly tiles: Tile[]) {
    tiles.forEach((t) => this._neighbors.set(t.id, this.neighborsOf(t)));
    this.dimension = Math.sqrt(tiles.length);
    this.assembledImage = Array.from({ length: this.dimension }, () =>
      Array.from({ length: this.dimension }, () => null as unknown as Tile)
    );
    this._corners = Array.from(this._neighbors.entries())
      .filter(([_, neighbors]) => neighbors.length === 2)
      .flatMap(([id, _]) => id);
  }

  getTile(id: string): Tile {
    return this.tiles.filter((t) => t.id === id)[0];
  }

  corners() {
    return this._corners;
  }

  neighbors(id: string) {
    return this._neighbors.get(id) || [];
  }

  neighborsOf(tile: Tile): Tile[] {
    return this.tiles.filter((t) => tile.neighborOf(t) === true);
  }

  placeTile(tile: Tile, row: number, col: number) {
    this.assembledImage[row][col] = tile;
    this.seen.add(tile.id);
  }

  orient(tile: Tile, row: number, col: number) {
    if (row >= this.dimension || col >= this.dimension) {
      return;
    }
    this.neighbors(tile.id).forEach((t) => {
      if (!this.seen.has(t.id)) {
        if (t.hasEdge(tile.edgeAt(SIDE.E))) {
          t.arrange(SIDE.W, tile.edgeAt(SIDE.E));
          this.placeTile(t, row, col + 1);
          this.orient(t, row, col + 1);
        } else if (t.hasEdge(tile.edgeAt(SIDE.S))) {
          t.arrange(SIDE.N, tile.edgeAt(SIDE.S));
          this.placeTile(t, row + 1, col);
          this.orient(t, row + 1, col);
        }
      }
    });
  }

  reassemble() {
    // Step 1: pick any corner
    const corner = this.getTile(this.corners()[0]);
    // Step 2: rotate corner into position
    const [se1, se2] = this.neighbors(corner.id).map((n) =>
      corner.sharedEdges(n)
    );
    for (let i = 0; i < 8; i++) {
      if (
        se1.includes(corner.edgeAt(SIDE.E)) &&
        se2.includes(corner.edgeAt(SIDE.S))
      ) {
        break;
      }

      if (i === 3) {
        corner.flip();
      } else {
        corner.rotate();
      }
    }
    // Step 3: place the corner piece and mark it as processed
    this.placeTile(corner, 0, 0);
    // Step 4: solve the rest of the puzzle
    this.orient(corner, 0, 0);
    return this.exportImage();
  }

  exportImage() {
    const tilesWithoutBorder = this.assembledImage.map((row) =>
      row.map((t) => t.removeBorders())
    );
    return tilesWithoutBorder
      .flatMap((t) => transpose(t))
      .map((t) => t.join(''));
  }

  toString() {
    return this.assembledImage
      .map((row) => row.map((t) => t.id).join(','))
      .join('\n');
  }
}

export { TileImage };
