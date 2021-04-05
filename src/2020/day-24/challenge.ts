import { difference, range } from 'ramda';

export type coord = [x: number, y: number, z: number];
const Direction: Record<string, coord> = {
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

export const enum TileState {
  NONE = 0,
  SELF = 1 << 0,
  NEIGHBOR1 = 1 << 1,
  NEIGHBOR2 = 1 << 2,
  NEIGHBOR3 = 1 << 3,
  NEIGHBOR4 = 1 << 4,
  NEIGHBOR5 = 1 << 5,
  NEIGHBOR6 = 1 << 6,
  NEIGHBOR7 = 1 << 7,
  NEIGHBOR8 = 1 << 8,
  NEIGHBOR9 = 1 << 9,
  NEIGHBOR10 = 1 << 10,
  NEIGHBOR11 = 1 << 11,
  NEIGHBOR12 = 1 << 12,
  NEIGHBOR13 = 1 << 13,
  NEIGHBOR14 = 1 << 14,
  NEIGHBOR15 = 1 << 15,
  NEIGHBOR16 = 1 << 16,
  NEIGHBOR17 = 1 << 17,
  NEIGHBOR18 = 1 << 18,
  NEIGHBOR19 = 1 << 19,
  NEIGHBOR20 = 1 << 20,
  NEIGHBOR21 = 1 << 21,
  NEIGHBOR22 = 1 << 22,
  NEIGHBOR23 = 1 << 23,
  NEIGHBOR24 = 1 << 24,
  NEIGHBOR25 = 1 << 25,
  NEIGHBOR26 = 1 << 26,
}

const getNeighborsMask = 0b111111111111111111111111110;
const getNeighborCount = (v: number) =>
  (v & getNeighborsMask).toString(2).replace(/0/g, '').trim().length;

const getMaskForValue = (v: number) => {
  const neighborVals = v >>> TileState.SELF;
  return neighborVals << TileState.SELF;
};

const moveTile = (startingCoord: coord, dir: directions) => {
  const direction = Direction[dir];
  const [x, y, z] = startingCoord;
  return [x + direction[0], y + direction[1], z + direction[2]];
};

const getPermutationsOfCoords = (coords: coord): coord[] => {
  // only six neighbors, use Directions
  let res: coord[] = [];
  [...Object.entries(Direction)].map(([k, v]) => {
    const [x, y, z] = coords;
    const newPos = [x + v[0], y + v[1], z + v[2]] as coord;
    res = [...res, [...newPos]];
  });
  return difference(res, [coords]);
};

const getBlackTiles = (ts: Map<string, TileState>) =>
  [...ts.entries()].filter(([k, v]) => {
    const self = v & TileState.SELF;
    return self === TileColor.BLACK;
  });

const getCoordListFromMap = (ts: Map<string, TileState>): string[] =>
  Array.from(ts.keys());

const flipTiles = (listOfTilesToFlip: string[][]) => {
  const tileMap = new Map<string, TileColor>();

  listOfTilesToFlip.forEach((instruction) => {
    let referenceTile = [0, 0, 0] as coord;
    instruction.forEach((dir, idx) => {
      const pos = moveTile(referenceTile, dir as directions) as coord;
      referenceTile = pos;
      if (idx === instruction.length - 1) {
        const existingValue = tileMap.get(pos.toString()) || TileColor.WHITE;
        tileMap.set(pos.toString(), existingValue ^ TileColor.BLACK);
      }
    });
  });
  return tileMap;
};

const calcNextGeneration = (
  tileState: Map<string, TileState>
): Map<string, TileState> => {
  const nextState = new Map<string, TileState>();
  for (const [key, val] of tileState.entries()) {
    const self = val & TileState.SELF;
    const neighborCount = getNeighborCount(val);
    if (neighborCount === 2) {
      nextState.set(key.toString(), 0b1);
    } else {
      if (self === TileColor.BLACK && neighborCount === 1) {
        nextState.set(key.toString(), 0b1);
      }
    }
  }

  return nextState;
};

const flipTilesConwayStyle = (
  startingTiles: Map<string, TileColor>,
  iterations = 100
) => {
  const tileMap = new Map<string, TileState>();

  const runIteration = (ct: coord[]) => {
    let it = 0;
    let currentBlackTiles = [...ct];
    let blackTileLookupList = ct.map((v) => v.toString());
    do {
      tileMap.clear();
      const processedCoord = new Set<string>();
      for (const pos of currentBlackTiles) {
        const adjList = getPermutationsOfCoords(pos);
        let selfNewVal = tileMap.get(pos.toString()) || 0b1;

        for (const aPos of adjList) {
          if (processedCoord.has(aPos.toString())) {
            continue;
          }
          let newVal = tileMap.get(aPos.toString()) || 0b0;
          if (blackTileLookupList.includes(aPos.toString())) {
            newVal |= 1 << TileState.NONE;
            const maskForSelfNewValue = getMaskForValue(selfNewVal);
            const idx = maskForSelfNewValue.toString(2).length;
            const selfMask = maskForSelfNewValue | (1 << idx);
            selfNewVal |= selfMask;
          }

          const maskForNewValue = getMaskForValue(newVal);
          const nIdx = maskForNewValue.toString(2).length;
          const mask = maskForNewValue | (1 << nIdx);
          newVal |= mask;

          tileMap.set(aPos.toString(), newVal);
        }

        tileMap.set(pos.toString(), selfNewVal);
        processedCoord.add(pos.toString());
      }
      const nextGen = calcNextGeneration(tileMap);
      blackTileLookupList = getCoordListFromMap(nextGen);
      currentBlackTiles = blackTileLookupList.map((v) => {
        const [x, y, z] = v.split(',');
        return [+x, +y, +z];
      });
      it++;
    } while (it <= iterations);
  };

  const st = [...startingTiles.entries()]
    .filter(([_, v]) => v === TileColor.BLACK)
    .map(([k, _]) => {
      const [x, y, z] = k.split(',');
      return [+x, +y, +z] as coord;
    });

  runIteration(st);

  return tileMap;
};

export {
  flipTiles,
  moveTile,
  flipTilesConwayStyle,
  calcNextGeneration,
  getPermutationsOfCoords,
  getBlackTiles,
  getNeighborCount,
  Direction,
};
