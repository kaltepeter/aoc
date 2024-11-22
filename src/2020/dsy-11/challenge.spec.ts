import { flatten } from 'ramda';
import {
  changeSeats,
  changeSeatsNewRules,
  getAdjacentSeats,
  getOccupiedSeats,
  getOccupiedVisibleSeats,
  getSeatCounts,
  runSeatChanges,
  runSeatChangesNewRules,
  Seat,
  SeatMap,
} from './challenge';
import {
  inputs,
  sample,
  samplePartII,
  samplePartIIRound2,
  sampleRound1,
} from './inputs';
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
      test(`should return ${expectedSeats.toString()}`, () => {
        const pos = position as [number, number];
        expect(getAdjacentSeats(seatMap, pos)).toEqual(expectedSeats);
      });
    }
  );

  test(`getSeatCounts()`, () => {
    const adjSeats = getAdjacentSeats(sample, [1, 3]);
    expect(getSeatCounts(adjSeats)).toEqual({
      [Seat.OCCUPIED]: 0,
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

  describe(`part II`, () => {
    test(`getOccupiedSeats`, () => {
      expect(getOccupiedSeats(samplePartII).rows[4]).toEqual([2, 8]);
    });

    test(`getOccupiedVisibleSeats`, () => {
      const foundSeats = getOccupiedVisibleSeats(samplePartII, [4, 3]);
      const foundSeatValues = flatten(Object.values(foundSeats.rows));
      expect(foundSeatValues.length).toBe(8);
      expect(Object.keys(foundSeats.rows).length).toBe(7);
    });

    test(`changeSeatsNewRules()`, () => {
      const round1Seats = changeSeatsNewRules(sampleRound1).seatMap[0].join('');
      const expectedRound1Seats = samplePartIIRound2[0].join('');
      expect(round1Seats).toEqual(expectedRound1Seats);
    });

    test(`runSeatChangesNewRules(sample)`, () => {
      const seatChanges = runSeatChangesNewRules(sample);
      expect(seatChanges.counts[Seat.OCCUPIED]).toBe(26);
    });

    test(`runSeatChangesNewRules(inputs)`, () => {
      const seatChanges = runSeatChangesNewRules(inputs);
      expect(seatChanges.counts[Seat.OCCUPIED]).toBe(2091);
    });
  });
});
