export type coord = [x: number, y: number, z: number];
export const Direction: Record<string, coord> = {
  e: [1, -1, 0],
  se: [0, -1, 1],
  sw: [-1, 0, 1],
  w: [-1, 1, 0],
  nw: [0, 1, -1],
  ne: [1, 0, -1],
};

export type directions = 'e' | 'se' | 'sw' | 'w' | 'nw' | 'ne';

export const enum TileColor {
  WHITE = 0,
  BLACK = 1,
}

const moveTile = (startingCoord: coord, dir: directions) => {
  const direction = Direction[dir];
  const [x, y, z] = startingCoord;
  return [x + direction[0], y + direction[1], z + direction[2]];
};

const flipTiles = (listOfTilesToFlip: string[][]) => {
  const tileMap = new Map<string, TileColor>();

  listOfTilesToFlip.forEach((instruction) => {
    let referenceTile = [0, 0, 0] as coord;
    instruction.forEach((dir, idx) => {
      const pos = moveTile(referenceTile, dir) as coord;
      referenceTile = pos;
      if (idx === instruction.length - 1) {
        const existingValue = tileMap.get(pos.toString()) || TileColor.WHITE;
        tileMap.set(pos.toString(), existingValue ^ TileColor.BLACK);
      }
    });
  });
  return tileMap;
};

export { flipTiles, moveTile };
