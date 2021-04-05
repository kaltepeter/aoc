import { flatten, groupBy, mapObjIndexed, slice } from 'ramda';

export const enum Seat {
  FLOOR = '.',
  UNOCCUPIED = 'L',
  OCCUPIED = '#',
}

export interface ISeatTracker {
  rows: Record<string, number[]>;
  cols?: Record<string, number[]>;
}

export type SeatMap = Seat[][];

const printSeatMap = (seatMap: SeatMap) => {
  console.log(seatMap.map((r) => r.join('')).join('\n'));
};

const inBounds = (seatMap: SeatMap, row: number, col: number) =>
  row >= 0 && row < seatMap.length && col >= 0 && col < seatMap[0].length;

const getAdjacentSeats = (
  seatMap: SeatMap,
  pos: [number, number]
): string[] => {
  const [row, seat] = pos;
  const startSeat = seat >= 1 ? seat - 1 : 0;
  const startRow = row >= 1 ? row - 1 : 0;
  const endRow = row < seatMap.length - 1 ? row + 1 : seatMap.length;
  let adjacentSeats: Seat[] = [];
  const pRow = slice(startRow, row, seatMap).flat(1);
  const curRow = slice(row, row + 1, seatMap).flat(1);
  const nRow = slice(endRow, endRow + 1, seatMap).flat(1);
  const prevRowSeats = slice(startSeat, seat + 2, pRow);
  const curRowSeats = slice(startSeat, seat, curRow).concat(
    slice(seat + 1, seat + 2, curRow)
  );
  const nextRowSeats = slice(startSeat, seat + 2, nRow);
  adjacentSeats = [...prevRowSeats, ...curRowSeats, ...nextRowSeats];

  return adjacentSeats;
};

const getOccupiedVisibleSeats = (
  seatMap: SeatMap,
  pos: [number, number]
): ISeatTracker => {
  const beforeRows = pos[0] > 0 ? seatMap.slice(0, pos[0]) : [];
  const curRow = seatMap.slice(pos[0], pos[0] + 1);
  const afterRows =
    pos[0] < seatMap.length ? seatMap.slice(pos[0] + 1, seatMap.length) : [];
  const visibleSeats: ISeatTracker = { rows: {} };

  const found = {
    before: {
      left: false,
      center: false,
      right: false,
    },
    center: {
      left: false,
      right: false,
    },
    after: {
      left: false,
      center: false,
      right: false,
    },
  };

  for (let rIdx = beforeRows.length - 1; rIdx >= 0; rIdx--) {
    const rowDelta = pos[0] - rIdx;
    const pCol = pos[1] - rowDelta;
    const nCol = pos[1] + rowDelta;
    if (found.before.left === false && beforeRows[rIdx][pCol] !== Seat.FLOOR) {
      if (!visibleSeats.rows[rIdx]) {
        visibleSeats.rows[rIdx] = [];
      }
      found.before.left = true;
      if (beforeRows[rIdx][pCol] === Seat.OCCUPIED) {
        visibleSeats.rows[rIdx] = [...visibleSeats.rows[rIdx], pCol];
      }
    }
    if (
      found.before.center === false &&
      beforeRows[rIdx][pos[1]] !== Seat.FLOOR
    ) {
      if (!visibleSeats.rows[rIdx]) {
        visibleSeats.rows[rIdx] = [];
      }
      found.before.center = true;
      if (beforeRows[rIdx][pos[1]] === Seat.OCCUPIED) {
        visibleSeats.rows[rIdx] = [...visibleSeats.rows[rIdx], pos[1]];
      }
    }
    if (found.before.right === false && beforeRows[rIdx][nCol] !== Seat.FLOOR) {
      if (!visibleSeats.rows[rIdx]) {
        visibleSeats.rows[rIdx] = [];
      }
      found.before.right = true;
      if (beforeRows[rIdx][nCol] === Seat.OCCUPIED) {
        visibleSeats.rows[rIdx] = [...visibleSeats.rows[rIdx], nCol];
      }
    }
    if (found.before.left && found.before.center && found.before.right) {
      break;
    }
  }

  for (let i = pos[1] - 1; i >= 0; i--) {
    if (found.center.left === false && curRow[0][i] !== Seat.FLOOR) {
      if (!visibleSeats.rows[pos[0]]) {
        visibleSeats.rows[pos[0]] = [];
      }
      found.center.left = true;
      if (curRow[0][i] === Seat.OCCUPIED) {
        visibleSeats.rows[pos[0]] = [...visibleSeats.rows[pos[0]], i];
      }
      break;
    }
  }

  for (let i = pos[1] + 1; i < curRow[0].length; i++) {
    if (found.center.right === false && curRow[0][i] !== Seat.FLOOR) {
      if (!visibleSeats.rows[pos[0]]) {
        visibleSeats.rows[pos[0]] = [];
      }
      found.center.right = true;
      if (curRow[0][i] === Seat.OCCUPIED) {
        visibleSeats.rows[pos[0]] = [...visibleSeats.rows[pos[0]], i];
      }
      break;
    }
  }

  for (let rIdx = 0; rIdx < afterRows.length; rIdx++) {
    const rowDelta = pos[0] + rIdx + 1;
    const pCol = pos[1] - rIdx - 1;
    const nCol = pos[1] + rIdx + 1;
    if (found.after.left === false && afterRows[rIdx][pCol] !== Seat.FLOOR) {
      if (!visibleSeats.rows[rowDelta]) {
        visibleSeats.rows[rowDelta] = [];
      }
      found.after.left = true;
      if (afterRows[rIdx][pCol] === Seat.OCCUPIED) {
        visibleSeats.rows[rowDelta] = [...visibleSeats.rows[rowDelta], pCol];
      }
    }
    if (
      found.after.center === false &&
      afterRows[rIdx][pos[1]] !== Seat.FLOOR
    ) {
      if (!visibleSeats.rows[rowDelta]) {
        visibleSeats.rows[rowDelta] = [];
      }
      found.after.center = true;
      if (afterRows[rIdx][pos[1]] === Seat.OCCUPIED) {
        visibleSeats.rows[rowDelta] = [...visibleSeats.rows[rowDelta], pos[1]];
      }
    }
    if (found.after.right === false && afterRows[rIdx][nCol] !== Seat.FLOOR) {
      if (!visibleSeats.rows[rowDelta]) {
        visibleSeats.rows[rowDelta] = [];
      }
      found.after.right = true;
      if (afterRows[rIdx][nCol] === Seat.OCCUPIED) {
        visibleSeats.rows[rowDelta] = [...visibleSeats.rows[rowDelta], nCol];
      }
    }
    if (found.after.left && found.after.center && found.after.right) {
      break;
    }
  }

  return visibleSeats;
};

const getOccupiedSeats = (seatMap: SeatMap): ISeatTracker => {
  const foundCoords: ISeatTracker = {
    rows: {},
    cols: {},
  };
  seatMap.forEach((row, rowIdx) => {
    row.forEach((col, colIdx) => {
      if (col === Seat.OCCUPIED) {
        if (foundCoords.rows[rowIdx]) {
          foundCoords.rows[rowIdx] = [...foundCoords.rows[rowIdx], colIdx];
        } else {
          foundCoords.rows[rowIdx] = [colIdx];
        }
      }
    });
  });

  return foundCoords;
};

const groupSeats = (seat: string) => {
  if (seat === Seat.OCCUPIED) {
    return Seat.OCCUPIED;
  } else if (seat === Seat.UNOCCUPIED) {
    return Seat.UNOCCUPIED;
  } else {
    return Seat.FLOOR;
  }
};

const getSeatCounts = (seatList: string[]): Record<string, number> => {
  const seatGroups = groupBy((s) => groupSeats(s), seatList);
  return mapObjIndexed<string[], number, string>(
    (counts, key, sg) => counts.length,
    seatGroups
  );
};

const changeSeats = (
  seatMap: SeatMap
): {
  seatMap: SeatMap;
  hasChanges: boolean;
  counts: Record<string, number>;
} => {
  const newSeatMap: SeatMap = [...seatMap].map((r) => [...r]);
  let adjacentSeats = [];
  let hasChanges = false;
  seatMap.forEach((row, rowIdx) => {
    row.forEach((seat, seatIdx) => {
      adjacentSeats = getAdjacentSeats(seatMap, [rowIdx, seatIdx]);
      const counts = getSeatCounts(adjacentSeats);
      if (seat === Seat.UNOCCUPIED && !counts[Seat.OCCUPIED]) {
        hasChanges = true;
        newSeatMap[rowIdx][seatIdx] = Seat.OCCUPIED;
      } else if (seat === Seat.OCCUPIED && counts[Seat.OCCUPIED] >= 4) {
        hasChanges = true;
        newSeatMap[rowIdx][seatIdx] = Seat.UNOCCUPIED;
      }
    });
  });

  const finalCounts = getSeatCounts(seatMap.flat(1));
  return { seatMap: newSeatMap, hasChanges, counts: finalCounts };
};

const changeSeatsNewRules = (
  seatMap: SeatMap
): {
  seatMap: SeatMap;
  hasChanges: boolean;
  counts: Record<string, number>;
} => {
  const newSeatMap: SeatMap = [...seatMap].map((r) => [...r]);
  let hasChanges = false;
  let foundSeats;
  seatMap.forEach((row, rowIdx) => {
    row.forEach((seat, seatIdx) => {
      foundSeats = getOccupiedVisibleSeats(seatMap, [rowIdx, seatIdx]);
      const counts = flatten(Object.values(foundSeats.rows)).length;
      if (seat === Seat.UNOCCUPIED && counts === 0) {
        hasChanges = true;
        newSeatMap[rowIdx][seatIdx] = Seat.OCCUPIED;
      } else if (seat === Seat.OCCUPIED && counts >= 5) {
        hasChanges = true;
        newSeatMap[rowIdx][seatIdx] = Seat.UNOCCUPIED;
      }
    });
  });

  const finalCounts = getSeatCounts(newSeatMap.flat(1));
  return { seatMap: newSeatMap, hasChanges, counts: finalCounts };
};

const runSeatChanges = (
  seatMap: SeatMap
): { seatMap: SeatMap; counts: Record<string, number> } => {
  let hasChanges = true;
  let curSeatMap = [...seatMap];
  let counts: Record<string, number>;
  do {
    const cs = changeSeats(curSeatMap);
    hasChanges = cs.hasChanges;
    curSeatMap = cs.seatMap;
    counts = cs.counts;
  } while (hasChanges === true);

  return { seatMap: curSeatMap, counts };
};

const runSeatChangesNewRules = (
  seatMap: SeatMap
): { seatMap: SeatMap; counts: Record<string, number> } => {
  let hasChanges = true;
  let curSeatMap = [...seatMap];
  let counts: Record<string, number>;
  do {
    const cs = changeSeatsNewRules(curSeatMap);
    hasChanges = cs.hasChanges;
    curSeatMap = cs.seatMap;
    counts = cs.counts;
  } while (hasChanges === true);

  return { seatMap: curSeatMap, counts };
};

export {
  changeSeats,
  getAdjacentSeats,
  getSeatCounts,
  groupSeats,
  runSeatChanges,
  getOccupiedSeats,
  changeSeatsNewRules,
  getOccupiedVisibleSeats,
  runSeatChangesNewRules,
};
