import { groupBy, mapObjIndexed, slice } from 'ramda';

export const enum Seat {
  FLOOR = '.',
  UNOCCUPIED = 'L',
  OCCUPIED = '#',
}

export type SeatMap = Seat[][];

const printSeatMap = (seatMap: SeatMap) => {
  console.log(seatMap.map((r) => r.join('')).join('\n'));
};

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

export {
  changeSeats,
  getAdjacentSeats,
  getSeatCounts,
  groupSeats,
  runSeatChanges,
};
