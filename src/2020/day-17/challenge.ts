import { difference, intersection, range, uniq } from 'ramda';

export type point = [number, number, number];
export type point4d = [number, number, number, number];
export type coordsList = point[];

export const enum States {
  ACTIVE = '#',
  INACTIVE = '.',
}

enum Flags {
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
const isEmpty = (v: number) => !(v > Flags.NONE.valueOf());
const getNeighborCount = (v: number) =>
  (v & getNeighborsMask).toString(2).replace(/0/g, '').trim().length;
const getLastSetBit = (v: number) => {
  const strVal = v.toString(2);
  const pos = strVal.indexOf('1');
  return pos > -1 ? strVal.length - 1 - pos : -1;
};

const getMaskForValue = (v: number) => {
  const neighborVals = v >>> Flags.SELF;
  return neighborVals << Flags.SELF;
};

export interface IPocketDimension {
  activeCubes: Set<point>;
  inactiveCubes: Set<point>;
}

const getPermutationsOfCoords = (coords: point): coordsList => {
  let res: coordsList = [];
  const [xRange, yRange, zRange] = coords.map((c) => range(c - 1, c + 2));

  for (const x of xRange) {
    for (const y of yRange) {
      for (const z of zRange) {
        res = [...res, [x, y, z]];
      }
    }
  }
  return difference(res, [coords]);
};

const getPermutationsOfCoordsFor4D = (coords: point4d): point4d[] => {
  let res: point4d[] = [];
  const [xRange, yRange, zRange, wRange] = coords.map((c) =>
    range(c - 1, c + 2)
  );

  for (const x of xRange) {
    for (const y of yRange) {
      for (const z of zRange) {
        for (const w of wRange) {
          res = [...res, [x, y, z, w]];
        }
      }
    }
  }
  return difference(res, [coords]);
};

const calcCoordsForActiveCubes = (boards: string[][][]) => {
  let activeCubes: coordsList = [];
  boards.forEach((b, zIndex) => {
    b.forEach((row, xIndex) => {
      row.forEach((cube, yIndex) => {
        if (cube === States.ACTIVE.toString()) {
          activeCubes = [...activeCubes, [xIndex, yIndex, zIndex]];
        }
      });
    });
  });
  return activeCubes;
};

const calcCoordsForActiveCubes4D = (boards: string[][][][]): point4d[] => {
  let activeCubes = [] as point4d[];
  boards.forEach((b, zIndex) => {
    b.forEach((w, wIndex) => {
      w.forEach((row, xIndex) => {
        row.forEach((cube, yIndex) => {
          if (cube === States.ACTIVE.toString()) {
            activeCubes = [...activeCubes, [xIndex, yIndex, zIndex, wIndex]];
          }
        });
      });
    });
  });
  return activeCubes;
};

// const printCubeState = (cubeState: string[][][]) => {
//   const printableState = cubeState
//     .map((depth) => depth.map((row) => row.join('')).join('\n'))
//     .join('\n\n');
//   console.log(printableState);
//   return printableState;
// };

const runCycle = (activeCubes: coordsList) => {
  const pocketDimension: IPocketDimension = {
    activeCubes: new Set<point>(),
    inactiveCubes: new Set<point>(),
  };
  const newActiveCubes: point[] = [];
  const newInactiveCubes: point[] = [];

  const neighbors: Set<point> = new Set(
    activeCubes.reduce<coordsList>(
      (acc, pos) =>
        (acc = [...acc, ...getPermutationsOfCoords(pos)] as coordsList),
      []
    )
  );
  neighbors.forEach((pos) => {
    const cubeNeighbors = getPermutationsOfCoords(pos);
    const cubeActiveNeighbors = intersection(cubeNeighbors, activeCubes);
    if (cubeActiveNeighbors.length === 3) {
      newActiveCubes.push(pos);
    } else {
      const isActive = intersection(activeCubes, [pos]).length > 0;
      if (cubeActiveNeighbors.length === 2 && isActive) {
        newActiveCubes.push(pos);
      } else {
        newInactiveCubes.push(pos);
      }
    }
  });
  pocketDimension.activeCubes = new Set(uniq(newActiveCubes));
  pocketDimension.inactiveCubes = new Set(uniq(newInactiveCubes));

  return pocketDimension;
};

const getCurrentCube = (cs: string[][][], [x, y, z]: point): States => {
  if (cs[z] && cs[z][x] && cs[z][x][y]) {
    return cs[z][x][y] as States;
  }
  return States.INACTIVE;
};

const calcPocketDimension = (cs: string[][]) => {
  // get initial list
  const activeCubes = calcCoordsForActiveCubes([cs]);
  const pocketDimension = runCycle(activeCubes);
  // start after initial list
  let newActiveList: coordsList = Array.from(pocketDimension.activeCubes);
  for (let i = 1; i < 6; i++) {
    newActiveList = Array.from(runCycle(newActiveList).activeCubes);
  }
  return newActiveList;
};

const calcNextGeneration = (
  pocketDimension: Map<string, number>
): Map<string, number> => {
  const currentDimension = pocketDimension.entries();
  const nextDimension = new Map<string, number>();
  for (const [key, val] of currentDimension) {
    const self = val & Flags.SELF;
    const neighborCount = getNeighborCount(val);
    if (self === Flags.SELF.valueOf()) {
      if (neighborCount !== 2 && neighborCount !== 3) {
        // nextDimension.set(key, 0b0)
      } else {
        nextDimension.set(key, 0b1);
      }
    } else {
      if (neighborCount === 3) {
        nextDimension.set(key, 0b1);
      }
    }
  }

  return nextDimension;
};

const getCoordListFromMap = (pocketDimension: Map<string, number>): string[] =>
  Array.from(pocketDimension.keys());

// count neighbors
const countResults = (pocketDimension: Map<string, number>): number =>
  Array.from(pocketDimension.values()).reduce(
    (acc, v) => (acc += getNeighborCount(v)),
    0
  );

const calcPocketDimensionFast = (
  cs: string[][],
  iterations: number = 1
): Map<string, number> => {
  const currentCubeState = [[], cs, []];
  const pocketDimension = new Map<string, number>();

  const runIteration = (ac: coordsList) => {
    let it = 0;
    let activeCubes = [...ac];
    let activeCubeLookupList = ac.map((v) => v.toString());
    do {
      pocketDimension.clear();
      const processedCoord = new Set<string>();
      for (const pos of activeCubes) {
        const neighbors = getPermutationsOfCoords(pos);
        let selfNewVal = pocketDimension.get(pos.toString()) || 0b1;

        // for each neighbor
        for (const nPos of neighbors) {
          if (processedCoord.has(nPos.toString())) {
            continue;
          }
          let newVal = pocketDimension.get(nPos.toString()) || 0b0; // default EMPTY
          //   // for self
          // const cube = getCurrentCube(currentCubeState, nPos);
          if (activeCubeLookupList.includes(nPos.toString())) {
            newVal |= 1 << Flags.NONE;
            // if neighbor is active, increment self counts
            const maskForSelfNewValue = getMaskForValue(selfNewVal);
            const idx = maskForSelfNewValue.toString(2).length;
            const selfMask = maskForSelfNewValue | (1 << idx);
            selfNewVal |= selfMask;
          }

          //   // // for the neighbors
          const maskForNewValue = getMaskForValue(newVal);
          const nIdx = maskForNewValue.toString(2).length;
          const mask = maskForNewValue | (1 << nIdx);
          newVal |= mask;

          pocketDimension.set(nPos.toString(), newVal);
          // processedCoord.add(nPos.toString());
        }

        pocketDimension.set(pos.toString(), selfNewVal);
        processedCoord.add(pos.toString());
      }
      // set next gen, resets
      const nextGen = calcNextGeneration(pocketDimension);
      activeCubeLookupList = getCoordListFromMap(nextGen);
      activeCubes = activeCubeLookupList.map((v) => {
        const [x, y, z] = v.split(',');
        return [+x, +y, +z];
      });
      it++;
    } while (it < iterations);
  };
  runIteration(calcCoordsForActiveCubes(currentCubeState));
  return pocketDimension;
};

const calcPocketDimensionFast4D = (
  cs: string[][],
  iterations: number = 1
): Map<string, number> => {
  const currentCubeState = [[[], cs, []]];
  const pocketDimension = new Map<string, number>();

  const runIteration = (ac: point4d[]) => {
    let it = 0;
    let activeCubes = [...ac];
    let activeCubeLookupList = ac.map((v) => v.toString());
    do {
      pocketDimension.clear();
      const processedCoord = new Set<string>();
      for (const pos of activeCubes) {
        const neighbors = getPermutationsOfCoordsFor4D(pos);
        let selfNewVal = pocketDimension.get(pos.toString()) || 0b1;

        // for each neighbor
        for (const nPos of neighbors) {
          if (processedCoord.has(nPos.toString())) {
            continue;
          }
          let newVal = pocketDimension.get(nPos.toString()) || 0b0; // default EMPTY
          //   // for self
          // const cube = getCurrentCube(currentCubeState, nPos);
          if (activeCubeLookupList.includes(nPos.toString())) {
            newVal |= 1 << Flags.NONE;
            // if neighbor is active, increment self counts
            const maskForSelfNewValue = getMaskForValue(selfNewVal);
            const idx = maskForSelfNewValue.toString(2).length;
            const selfMask = maskForSelfNewValue | (1 << idx);
            selfNewVal |= selfMask;
          }

          //   // // for the neighbors
          const maskForNewValue = getMaskForValue(newVal);
          const nIdx = maskForNewValue.toString(2).length;
          const mask = maskForNewValue | (1 << nIdx);
          newVal |= mask;

          pocketDimension.set(nPos.toString(), newVal);
          // processedCoord.add(nPos.toString());
        }

        pocketDimension.set(pos.toString(), selfNewVal);
        processedCoord.add(pos.toString());
      }
      // set next gen, resets
      const nextGen = calcNextGeneration(pocketDimension);
      activeCubeLookupList = getCoordListFromMap(nextGen);
      activeCubes = activeCubeLookupList.map((v) => {
        const [x, y, z, w] = v.split(',');
        return [+x, +y, +z, +w];
      });
      it++;
    } while (it < iterations);
  };
  runIteration(calcCoordsForActiveCubes4D(currentCubeState));
  return pocketDimension;
};

export {
  getPermutationsOfCoords,
  calcCoordsForActiveCubes,
  runCycle,
  calcPocketDimension,
  calcPocketDimensionFast,
  getNeighborCount,
  isEmpty,
  getCurrentCube,
  getLastSetBit,
  Flags,
  getMaskForValue,
  countResults,
  calcNextGeneration,
  getPermutationsOfCoordsFor4D,
  calcPocketDimensionFast4D,
  calcCoordsForActiveCubes4D,
};
