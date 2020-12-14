import {
  changeSeats,
  getAdjacentSeats,
  getSeatCounts,
  runSeatChanges,
  Seat,
  SeatMap,
} from './challenge';
import { inputs, sample, sampleRound1 } from './inputs';
describe(`Day 11: Seating System`, () => {
  test(`processSeatMap()`, () => {
    expect(sample.length).toBe(10);
    expect(sample[0].length).toBe(10);
    expect(sample[1][0]).toBe(Seat.UNOCCUPIED);
  });

  describe.each([
    [sample, [0, 0], ['.', 'L', 'L']],
    [sample, [1, 1], ['L', '.', 'L', 'L', 'L', 'L', '.', 'L']],
    [sample, [0, 1], ['L', 'L', 'L', 'L', 'L']],
    [sample, [9, 2], ['.', 'L', 'L', '.', 'L']],
  ])(
    `getAdjacentSeats(%i, %j)`,
    (seatMap: SeatMap, position: number[], expectedSeats: string[]) => {
      test(`should return ${expectedSeats}`, () => {
        const pos = position as [number, number];
        expect(getAdjacentSeats(seatMap, pos)).toEqual(expectedSeats);
      });
    }
  );

  test(`getSeatCounts()`, () => {
    const adjSeats = getAdjacentSeats(sample, [1, 3]);
    expect(getSeatCounts(adjSeats)).toEqual({
      [Seat.FLOOR]: 2,
      [Seat.UNOCCUPIED]: 6,
    });
  });

  test(`changeSeats`, () => {
    const round1Seats = changeSeats(sample).seatMap[0].join('');
    const expectedRound1Seats = sampleRound1[0].join('');
    expect(round1Seats).toEqual(expectedRound1Seats);
  });

  test(`runSeatChanges(sample)`, () => {
    const seatChanges = runSeatChanges(sample);
    expect(seatChanges.counts[Seat.OCCUPIED]).toBe(37);
  });

  test.skip(`runSeatChanges(inputs)`, () => {
    const seatChanges = runSeatChanges(inputs);
    expect(seatChanges.counts[Seat.OCCUPIED]).toBe(2386);
  });
});
