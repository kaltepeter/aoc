import { flatten } from 'ramda';

const totalRows = 128;
const totalSeatsPerRow = 8;

export interface ISeat {
  row: number;
  seat: number;
}

const calcDelta = (range: [number, number]) => range[1] - range[0];

const getLowerHalf = (range: [number, number]): [number, number] => [
  range[0],
  Math.floor(range[1] - calcDelta(range) / 2),
];

const getUpperHalf = (range: [number, number]) => [
  Math.floor(range[1] + 1 - calcDelta(range) / 2),
  range[1],
];

const calcSeatId = (seat: ISeat): number => seat.row * 8 + seat.seat;

const parseSeat = (code: string): ISeat | undefined => {
  let curRowRange = [0, totalRows - 1];
  let curSeatRange = [0, totalSeatsPerRow - 1];
  const path = code.split('');
  for (const p of path) {
    switch (p) {
      case 'F':
        curRowRange = getLowerHalf([curRowRange[0], curRowRange[1]]);
        break;
      case 'L':
        curSeatRange = getLowerHalf([curSeatRange[0], curSeatRange[1]]);
        break;
      case 'B':
        curRowRange = getUpperHalf([curRowRange[0], curRowRange[1]]);
        break;
      case 'R':
        curSeatRange = getUpperHalf([curSeatRange[0], curSeatRange[1]]);
        break;
      default:
        console.error('Not found');
    }
  }
  if (
    curRowRange[0] === curRowRange[1] &&
    curSeatRange[0] === curSeatRange[1]
  ) {
    return { row: curRowRange[0], seat: curSeatRange[0] };
  } else {
    console.error(
      `Seat not found. row: ${curRowRange.toString()}, seat: ${curSeatRange.toString()}`
    );
  }
};

const calcMaxSeatId = (seatIds: number[]) => Math.max(...seatIds);

const calcSeatIdsForListOfSeats = (seats: ISeat[]) =>
  seats.map((s) => calcSeatId(s));

const parseListOfSeats = (listOfSeats: string[]): ISeat[] =>
  listOfSeats.map((seatPath) => parseSeat(seatPath) as ISeat);

const generateSeats = () =>
  new Array<string[]>(128).fill(new Array<string>(8).fill('.'));

const calcAvailableSeatIds = (): number[] =>
  flatten(
    generateSeats().map((row: string[], idx: number) =>
      row.map((_, pos) => calcSeatId({ row: idx, seat: pos }))
    )
  );

const printSeats = (seats: string[][]): string =>
  seats.map((r) => r.join('')).join('\n');

export {
  generateSeats,
  printSeats,
  parseSeat,
  getLowerHalf,
  getUpperHalf,
  totalRows,
  totalSeatsPerRow,
  calcSeatId,
  parseListOfSeats,
  calcSeatIdsForListOfSeats,
  calcMaxSeatId,
  calcAvailableSeatIds,
};
