import { mergeDeepRight } from 'ramda';

export const enum Action {
  NORTH = 'N',
  SOUTH = 'S',
  EAST = 'E',
  WEST = 'W',
  LEFT = 'L',
  RIGHT = 'R',
  FORWARD = 'F',
}

export enum Direction {
  N = 0,
  E = 90,
  S = 180,
  W = 270,
}

export interface IShipCoords {
  waypoint: { x: number; y: number };
  ship: { x: number; y: number };
  dir: Direction;
}

const calcDirs = (startDir: Direction, val: number) => {
  let newDir = startDir + val;
  newDir = newDir % 360;
  if (newDir >= 360) {
    newDir -= 360;
  } else if (newDir < 0) {
    newDir += 360;
  }

  return newDir;
};

const getActionForDirection = (dir: Direction, opposite: boolean = false) => {
  switch (dir) {
    case Direction.N:
      return opposite ? Action.SOUTH : Action.NORTH;
    case Direction.E:
      return opposite ? Action.WEST : Action.EAST;
    case Direction.S:
      return opposite ? Action.NORTH : Action.SOUTH;
    case Direction.W:
      return opposite ? Action.EAST : Action.WEST;
    default:
      break;
  }
};

export type CHANGE_DIRECTION = Action.LEFT | Action.RIGHT;

export type Instructions = Array<[Action, number]>;

export interface ITrackPath {
  [Action.NORTH]: number;
  [Action.SOUTH]: number;
  [Action.EAST]: number;
  [Action.WEST]: number;
  [Action.LEFT]: number;
  [Action.RIGHT]: number;
  [Action.FORWARD]: number;
}

const START_DIR = Direction.E;

const calcShipPath = (instructions: Instructions) => {
  const trackPath: ITrackPath = {
    [Action.NORTH]: 0,
    [Action.SOUTH]: 0,
    [Action.EAST]: 0,
    [Action.WEST]: 0,
    [Action.LEFT]: 0,
    [Action.RIGHT]: 0,
    [Action.FORWARD]: 0,
  };
  let curDirection = START_DIR;
  let x = 0;
  let y = 0;
  instructions.forEach(([action, value]) => {
    switch (action) {
      case Action.FORWARD:
        switch (curDirection) {
          case Direction.N:
            y -= value;
            trackPath[Action.NORTH] -= value;
            break;
          case Direction.S:
            y += value;
            trackPath[Action.SOUTH] += value;
            break;
          case Direction.E:
            x += value;
            trackPath[Action.EAST] += value;
            break;
          case Direction.W:
            x -= value;
            trackPath[Action.WEST] -= value;
            break;
          default:
            break;
        }
        break;
      case Action.NORTH:
        trackPath[action] -= value;
        y -= value;
        break;
      case Action.SOUTH:
        trackPath[action] += value;
        y += value;
        break;
      case Action.EAST:
        trackPath[action] += value;
        x += value;
        break;
      case Action.WEST:
        trackPath[action] -= value;
        x -= value;
        break;
      case Action.RIGHT:
        curDirection = calcDirs(curDirection, value);
        break;
      case Action.LEFT:
        curDirection = calcDirs(curDirection, -value);
        break;
      default:
        // console.log('no action');
        break;
    }
  });
  return trackPath;
};

const getManhattanDistance = (trackPath: ITrackPath) => {
  const y = Math.abs(trackPath.S + trackPath.N);
  const x = Math.abs(trackPath.E + trackPath.W);
  return x + y;
};

const rotateWaypoint = (
  coords: IShipCoords,
  count: number,
  rotDir: 'R' | 'L'
) => {
  const { x, y } = coords.waypoint;
  const newCoords = { waypoint: { x, y }, dir: coords.dir };

  if (rotDir === 'L') {
    for (let i = 0; i < count; i++) {
      newCoords.waypoint = { x: newCoords.waypoint.y, y: newCoords.waypoint.x };
      newCoords.waypoint.y *= -1;
    }
    newCoords.dir = calcDirs(coords.dir, -(count * 90));
  } else {
    for (let i = 0; i < count; i++) {
      newCoords.waypoint = { x: newCoords.waypoint.y, y: newCoords.waypoint.x };
      newCoords.waypoint.x *= -1;
    }
    newCoords.dir = calcDirs(coords.dir, count * 90);
  }
  return mergeDeepRight(coords, newCoords);
};

const getWayPoints = (instructions: Instructions): number => {
  let coords: IShipCoords = {
    waypoint: { x: 10, y: -1 },
    ship: { x: 0, y: 0 },
    dir: Direction.E,
  };
  let count = Direction.E;
  instructions.forEach(([action, value]) => {
    switch (action) {
      case Action.FORWARD:
        coords.ship.y += value * coords.waypoint.y;
        coords.ship.x += value * coords.waypoint.x;
        break;
      case Action.NORTH:
        coords.waypoint.y -= value;
        break;
      case Action.SOUTH:
        coords.waypoint.y += value;
        break;
      case Action.EAST:
        coords.waypoint.x += value;
        break;
      case Action.WEST:
        coords.waypoint.x -= value;
        break;
      case Action.RIGHT:
        count = value / 90;
        coords = mergeDeepRight(coords, rotateWaypoint(coords, count, 'R'));
        break;
      case Action.LEFT:
        count = value / 90;
        coords = mergeDeepRight(coords, rotateWaypoint(coords, count, 'L'));
        break;
      default:
        // console.log('no action');
        break;
    }
    // console.log(`action: ${action}, value: ${value}`, coords);
  });
  return Math.abs(coords.ship.x) + Math.abs(coords.ship.y);
};

export {
  calcShipPath,
  calcDirs,
  getManhattanDistance,
  getWayPoints,
  rotateWaypoint,
};
