import {
  getErrorRate,
  getInvalidTicketValues,
  IRuleSet,
  processRules,
} from './challenge';
import { inputs, sample } from './inputs';
describe(`Day 16: Ticket Translation`, () => {
  test(`processTickets()`, () => {
    expect(sample.rules.length).toBe(3);
    expect(sample.ticket.length).toBe(3);
    expect(sample.nearbyTickets.length).toBe(4);

    expect(inputs.rules.length).toBe(20);
    expect(inputs.ticket.length).toBe(20);
    expect(inputs.nearbyTickets.length).toBe(235);
  });

  test(`getInvalidTicketValues(sample)`, () => {
    expect(getInvalidTicketValues(sample)).toEqual([4, 55, 12]);
  });

  test(`getErrorRate([4,55,12])`, () => {
    expect(getErrorRate([4, 55, 12])).toBe(71);
  });

  test(`getErrorRate(inputs)`, () => {
    const inputVals = getInvalidTicketValues(inputs);
    expect(getErrorRate(inputVals)).toBe(22073);
  });

  describe.each([
    ['class', 0, 1, true],
    ['class', 0, 3, true],
    ['class', 0, 4, false],
    // ['class', 1, 5, true],
    ['class', 1, 7, true],
    ['class', 1, 9, false],
  ])(
    `processRules(sample.rules)['%s'][%i](%i)`,
    (
      rule: string,
      rangePos: number,
      testValue: number,
      expectedResult: boolean
    ) => {
      let ruleList: IRuleSet;

      beforeEach(() => {
        ruleList = processRules(sample.rules);
      });

      test(`should return ${expectedResult}`, () => {
        expect(ruleList[rule][rangePos](testValue)).toBe(expectedResult);
      });
    }
  );
});
