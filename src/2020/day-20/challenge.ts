import { intersection, pair } from 'ramda';

export class Tile {
  edges = new Set<string>();
  neighbors = new Set<string>();

  constructor(tileData: string) {
    this.edges = getEdgesForTile(tileData);
  }

  sharedEdges(tile: Tile) {
    return intersection(Array.from(this.edges), Array.from(tile.edges));
  }

  neighborOf(tile: Tile) {
    return this !== tile && this.sharedEdges(tile).length > 0;
  }
}

const getEdgesForTile = (tile: string): Set<string> => {
  const rows = tile.split(/\n/);
  const firstCol = tile.match(/^./gm);
  const lastCol = tile.match(/.$/gm);
  let edges = [rows.slice(0)[0], rows.slice(rows.length - 1)[0]];
  if (firstCol) {
    edges.push(firstCol.join('').trim());
  }
  if (lastCol) {
    edges.push(lastCol.join('').trim());
  }
  const reversed = edges.map((s) => [...s].reverse().join(''));
  edges = [...edges, ...reversed];
  return new Set(edges);
};

const processTiles = (inputs: string[][]) => {
  const tileMap = inputs.reduce((acc, [tile, tileBoard]) => {
    acc.set(tile, new Tile(tileBoard));
    return acc;
  }, new Map<string, Tile>());
  tileMap.forEach((tile, k) => {
    const otherTiles = new Map(tileMap);
    otherTiles.delete(k);
    otherTiles.forEach((tile2, k2) => {
      if (tile.neighborOf(tile2)) {
        tile.neighbors.add(k2);
      }
    });
  });
  return tileMap;
};

const getCorners = (tileMap: Map<string, Tile>): string[] => {
  return Array.from(tileMap.entries())
    .filter(([_, tile]) => tile.neighbors.size === 2)
    .map(([tileId, _]) => tileId);
};

const calcResult = (corners: string[]): number => {
  return corners.map((v) => +v).reduce((acc, v) => (acc *= v), 1);
};

export { processTiles, getEdgesForTile, getCorners, calcResult };
