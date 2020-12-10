import {
  countBags,
  findBagsThatHoldAColor,
  getBagsForChildren,
  getListOfBagsThatHoldAColor,
  stopBags,
  walkListOfBags,
} from './challenge';
import { inputs, sampleData } from './inputs';

describe(`7: Handy Haversacks`, () => {
  test(`sampleData has 9 rules`, () => {
    expect(sampleData.length).toBe(9);
  });

  describe.each([
    ['shiny gold', 2],
    ['bright white', 2],
    ['faded blue', 3],
    ['light red', 0],
    ['dark orange', 0],
    ['muted yellow', 2],
    ['dark olive', 1],
    ['vibrant plum', 1],
    ['dotted black', 2],
  ])(
    `findBagsThatHoldAColor(%s)`,
    (bagColor: string, expectedNumberOfBags: number) => {
      test(`should return ${expectedNumberOfBags}`, () => {
        expect(findBagsThatHoldAColor(sampleData, bagColor).length).toEqual(
          expectedNumberOfBags
        );
      });
    }
  );
  test(`walkListOfBags() should return list of bags`, () => {
    expect(Object.keys(walkListOfBags(sampleData))).toEqual([
      'light red',
      'muted yellow',
      'bright white',
      'dark orange',
      'shiny gold',
      'faded blue',
      'vibrant plum',
      'dark olive',
      'dotted black',
    ]);
  });

  describe.each([
    ['shiny gold', 4],
    ['faded blue', 7],
    ['vibrant plum', 5],
  ])(
    `findAllBagsThatHoldAColor(%s)`,
    (bagColor: string, expectedNumberOfBags: number) => {
      test(`should return ${expectedNumberOfBags}`, () => {
        const bagList = walkListOfBags(sampleData);
        expect(getListOfBagsThatHoldAColor(bagColor, bagList)).toEqual(
          expectedNumberOfBags
        );
      });
    }
  );

  test(`countBags()`, () => {
    expect(
      countBags(
        [
          {
            name: 'muted yellow',
            counted: false,
            children: [],
          },
        ],
        0
      )
    ).toBe(1);
  });

  test(`inputs has 20 rules`, () => {
    const bagList = walkListOfBags(inputs);
    expect(getListOfBagsThatHoldAColor('shiny gold', bagList)).toEqual(155);
  });

  test(`stopBags(rules)`, () => {
    expect(stopBags(inputs).length).toBe(10);
  });

  test(`getBagsForChildren(' 5 faded blue bags, 6 dotted black bags.')`, () => {
    expect(
      getBagsForChildren(' 5 faded blue bags, 6 dotted black bags.')
    ).toEqual(['faded blue', 'dotted black']);
  });
});
