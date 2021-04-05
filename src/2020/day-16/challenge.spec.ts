import { fromPairs, objOf, transpose } from 'ramda';
import {
  getErrorRate,
  getInvalidTicketValues,
  getValidTickets,
  IRuleSet,
  processRules,
  getTicketFieldList,
  processTickets,
  validateColumn,
  getDepartureFieldsResult,
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

  describe(`Part II`, () => {
    test(`getValidTickets(sample)`, () => {
      expect(getValidTickets(sample).nearbyTickets.length).toBe(2);
    });

    test(`getValidTickets(inputs)`, () => {
      expect(getValidTickets(inputs).nearbyTickets.length).toBe(191);
    });

    test(`getTicketFieldList(sample)`, () => {
      const ticketList = getValidTickets(sample);
      const rules = processRules(ticketList.rules);
      const fieldValues = transpose(ticketList.nearbyTickets);
      const list = getTicketFieldList(rules, fieldValues);
      expect(fieldValues.length).toBe(3);
      expect(fieldValues[0].length).toBe(2);
    });

    test(`processTickets(sample)`, () => {
      const ticketList = getValidTickets(sample);
      const fieldList = processTickets(ticketList);
      expect(fieldList).toEqual({ class: 1, row: 0, seat: 2 });
    });

    test(`processTickets(inputs)`, () => {
      const ticketList = getValidTickets(inputs);
      expect(processTickets(ticketList)).toEqual({
        type: 5,
        'arrival platform': 12,
        train: 10,
        class: 1,
        duration: 18,
        seat: 13,
        'arrival location': 15,
        zone: 19,
        route: 17,
        row: 8,
        'departure platform': 9,
        'departure time': 3,
        'departure date': 6,
        'departure track': 7,
        'departure station': 14,
        'departure location': 16,
        price: 0,
        'arrival track': 2,
        wagon: 4,
        'arrival station': 11,
      });
    });

    test(`getDepartureFieldsResult()`, () => {
      const fieldList = {
        type: 5,
        'arrival platform': 12,
        train: 10,
        class: 1,
        duration: 18,
        seat: 13,
        'arrival location': 15,
        zone: 19,
        route: 17,
        row: 8,
        'departure platform': 9,
        'departure time': 3,
        'departure date': 6,
        'departure track': 7,
        'departure station': 14,
        'departure location': 16,
        price: 0,
        'arrival track': 2,
        wagon: 4,
        'arrival station': 11,
      };
      const ticketList = getValidTickets(inputs);
      expect(getDepartureFieldsResult(fieldList, ticketList)).toBeGreaterThan(
        254016
      );
      expect(getDepartureFieldsResult(fieldList, ticketList)).toBe(
        1346570764607
      );
    });

    test(`getTicketFieldList(inputs)`, () => {
      const ticketList = getValidTickets(inputs);
      const rules = processRules(ticketList.rules);
      const fieldValues = transpose(ticketList.nearbyTickets);
      const list = getTicketFieldList(rules, fieldValues);
      expect(fieldValues.length).toBe(20);
      expect(fieldValues[0].length).toBe(191);
      expect(list.length).toBe(20);
    });

    test(`validateColumn()`, () => {
      const ticketList = getValidTickets(inputs);
      const rules = processRules(ticketList.rules);
      const fieldValues = transpose(ticketList.nearbyTickets);
      expect(Array.from(validateColumn(fieldValues[0], rules))).toEqual([
        'departure location',
        'departure station',
        'departure platform',
        'departure track',
        'departure date',
        'departure time',
        'arrival location',
        'arrival platform',
        'class',
        'duration',
        'price',
        'route',
        'row',
        'seat',
        'train',
        'type',
        'zone',
      ]);
      expect(Array.from(validateColumn(fieldValues[1], rules))).toEqual([
        'arrival platform',
        'class',
        'train',
        'type',
      ]);
    });
  });
});
