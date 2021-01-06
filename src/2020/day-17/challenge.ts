import { range, intersection, difference, uniq } from 'ramda';

export type point = [number, number, number];
export type coordsList = point[];

export const enum States {
  ACTIVE = '#',
  INACTIVE = '.',
}

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

const calcCoordsForActiveCubes = (...boards: string[][][]) => {
  let activeCubes: coordsList = [];
  boards.forEach((b, zIndex) => {
    b.forEach((row, xIndex) => {
      row.forEach((cube, yIndex) => {
        if (cube === States.ACTIVE) {
          activeCubes = [...activeCubes, [xIndex, yIndex, zIndex]];
        }
      });
    });
  });
  return activeCubes;
};

const printCubeState = (cubeState: string[][][]) => {
  const printableState = cubeState
    .map((depth) => {
      return depth.map((row) => row.join('')).join('\n');
    })
    .join('\n\n');
  console.log(printableState);
  return printableState;
};

const runCycle = (activeCubes: coordsList) => {
  let pocketDimension: IPocketDimension = {
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

const calcPocketDimension = (cs: string[][]) => {
  printCubeState([cs]);
  // get initial list
  let activeCubes = calcCoordsForActiveCubes(cs);
  let pocketDimension = runCycle(activeCubes);
  // start after initial list
  let newActiveList: coordsList = Array.from(pocketDimension.activeCubes);
  for (let i = 1; i < 6; i++) {
    newActiveList = Array.from(runCycle(newActiveList).activeCubes);
  }
  return newActiveList;
};

export {
  getPermutationsOfCoords,
  calcCoordsForActiveCubes,
  runCycle,
  calcPocketDimension,
};
