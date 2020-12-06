import {
  calcMaxSeatId,
  calcSeatId,
  calcSeatIdsForListOfSeats,
  getLowerHalf,
  getUpperHalf,
  ISeat,
  parseListOfSeats,
  parseSeat,
  totalRows,
  totalSeatsPerRow,
} from './challenge';
import { inputs } from './inputs';
describe(`5: Plane boarding`, () => {
  beforeEach(() => {});

  test(`calcSeatId({row: 44, seat: 5})`, () => {
    expect(calcSeatId({ row: 44, seat: 5 })).toBe(357);
  });

  test(`returns 761 totalSeats, max seatId: 861`, () => {
    const seatList = [...inputs];
    const seats = parseListOfSeats(seatList);
    const seatIds = calcSeatIdsForListOfSeats(seats);
    expect(seatList.length).toBe(761);
    expect(seatIds.length).toBe(761);
    expect(calcMaxSeatId(seatIds)).toBe(861);
  });

  describe.each([
    ['FBFBBFFRLR', { row: 44, seat: 5 }, 357],
    ['BFFFBBFRRR', { row: 70, seat: 7 }, 567],
    ['FFFBBBFRRR', { row: 14, seat: 7 }, 119],
    ['BBFFBBFRLL', { row: 102, seat: 4 }, 820],
  ])(
    'seat is "%s"',
    (value: string, expectedSeat: ISeat, expectedSeatId: number) => {
      test(`parseSeat('${value}') returns ${JSON.stringify(
        expectedSeat
      )}`, () => {
        const seat = parseSeat(value);
        expect(seat).toEqual(expectedSeat);
      });

      test(`calcSeatId(${JSON.stringify(
        expectedSeat
      )}) returns ${expectedSeatId}`, () => {
        const seatId = calcSeatId(expectedSeat);
        expect(seatId).toEqual(expectedSeatId);
      });
    }
  );

  test(`getLowerHalf() of 'F'`, () => {
    expect(getLowerHalf([0, totalRows - 1])).toEqual([0, 63]);
  });

  test(`getUpperHalf() of 'FB'`, () => {
    expect(getUpperHalf([0, 63])).toEqual([32, 63]);
  });

  test(`getLowerHalf() of 'FBF'`, () => {
    expect(getLowerHalf([32, 63])).toEqual([32, 47]);
  });

  test(`getUpperHalf() of 'FBFB'`, () => {
    expect(getUpperHalf([32, 47])).toEqual([40, 47]);
  });

  test(`getUpperHalf() of 'FBFBB'`, () => {
    expect(getUpperHalf([40, 47])).toEqual([44, 47]);
  });

  test(`getLowerHalf() of 'FBFBBF'`, () => {
    expect(getLowerHalf([44, 47])).toEqual([44, 45]);
  });

  test(`getLowerHalf() of 'FBFBBFF'`, () => {
    expect(getLowerHalf([44, 45])).toEqual([44, 44]);
  });

  test(`getUpperHalf() of 'R'`, () => {
    expect(getUpperHalf([0, totalSeatsPerRow - 1])).toEqual([4, 7]);
  });

  test(`getLowerHalf() of 'RL'`, () => {
    expect(getLowerHalf([4, 7])).toEqual([4, 5]);
  });

  test(`getUpperHalf() of 'RLR'`, () => {
    expect(getUpperHalf([4, 5])).toEqual([5, 5]);
  });
});
