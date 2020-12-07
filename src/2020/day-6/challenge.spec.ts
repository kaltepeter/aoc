import {
  countAllYessesForGroup,
  countForGroup,
  totalAllYessesForAllGroups,
  totalAllYessesForGroup,
  totalYessesForGroup,
} from './challenge';
import { inputs, sampleData } from './inputs';

describe(`6: Custom Customs`, () => {
  test(`sampleData has 5 groups`, () => {
    expect(sampleData.length).toBe(5);
    expect(sampleData[0].length).toBe(1);
    expect(sampleData[0][0].length).toBe(3);
  });

  test(`countForGroup(group)`, () => {
    expect(countForGroup(sampleData[0]).size).toBe(3);
  });

  describe.each([
    [sampleData[0], 1, 3],
    [sampleData[1], 3, 3],
    [sampleData[2], 2, 3],
    [sampleData[3], 4, 1],
    [sampleData[4], 1, 1],
  ])(
    `group answered %j for %i people`,
    (
      value: string[][],
      expectedPeopleCount: number,
      expectedYesses: number
    ) => {
      test(`number of people is ${expectedPeopleCount}`, () => {
        expect(value.length).toEqual(expectedPeopleCount);
      });

      test(`expectedYesses is ${expectedYesses}`, () => {
        expect(countForGroup(value).size).toEqual(expectedYesses);
      });
    }
  );

  test(`count totalYesses for Group`, () => {
    expect(totalYessesForGroup(sampleData)).toBe(11);
  });

  test(`count totalYesses for puzzle input`, () => {
    expect(inputs.length).toBe(465);
    expect(countForGroup(inputs[0])).toEqual(
      new Set(['v', 'x', 'n', 'c', 'l', 'm', 'b'])
    );
    expect(countForGroup(inputs[464])).toEqual(new Set(['c', 'o']));
    expect(465 * 26).toBeGreaterThanOrEqual(6443);
    expect(totalYessesForGroup(inputs)).toBe(6443);
  });

  describe('part II', () => {
    test(`countAllYessesForGroup(group)`, () => {
      expect(countAllYessesForGroup(sampleData[0])).toEqual({
        a: 1,
        b: 1,
        c: 1,
      });
    });

    describe.each([
      [sampleData[0], 1, 3],
      [sampleData[1], 3, 0],
      [sampleData[2], 2, 1],
      [sampleData[3], 4, 1],
      [sampleData[4], 1, 1],
    ])(
      `group answered %j for %i people`,
      (
        value: string[][],
        expectedPeopleCount: number,
        expectedYesses: number
      ) => {
        test(`number of people is ${expectedPeopleCount}`, () => {
          expect(value.length).toEqual(expectedPeopleCount);
        });

        test(`expectedYesses is ${expectedYesses}`, () => {
          expect(totalAllYessesForGroup(value.length, value).length).toEqual(
            expectedYesses
          );
        });
      }
    );

    test(`count totalYesses for Group`, () => {
      expect(totalAllYessesForAllGroups(sampleData)).toBe(6);
    });

    test(`count totalYesses for puzzle input`, () => {
      expect(inputs.length).toBe(465);
      expect(countAllYessesForGroup(inputs[0])).toEqual({
        b: 1,
        c: 1,
        l: 1,
        m: 1,
        n: 1,
        v: 5,
        x: 2,
      });
      expect(countAllYessesForGroup(inputs[464])).toEqual({ c: 2, o: 1 });
      expect(totalAllYessesForAllGroups(inputs)).toBe(3232);
    });
  });
});
