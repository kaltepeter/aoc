import {
  countAllergens,
  findIngredientsNotInAllergenList,
  getAllergenList,
  getFoodList,
  processAllergens,
} from './challenge';
import { inputs, sample } from './inputs';
describe(`Day 21: Allergen Assessment`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(4);
  });

  it(`should get list of ingredients and allergens`, () => {
    const list = getFoodList(sample);
    expect(list.length).toEqual(4);
    expect(list[0]).toEqual({
      ingredients: ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'],
      allergens: ['dairy', 'fish'],
    });
  });

  it(`should return a tracker of possible allergens`, () => {
    const list = getFoodList(sample);

    expect(getAllergenList(list).get('fish')).toEqual([
      'mxmxvkd',
      'kfcds',
      'sqjhc',
      'nhms',
      'sbzzf',
    ]);
  });

  it(`should get list not in allergen list`, () => {
    const list = getFoodList(sample);
    const allergenList = getAllergenList(list);
    expect(findIngredientsNotInAllergenList(list, allergenList)).toEqual(
      jasmine.arrayContaining(['kfcds', 'nhms', 'sbzzf', 'trh'])
    );
  });

  it(`processAllergens`, () => {
    const list = getFoodList(sample);
    const allergenList = getAllergenList(list);
    expect(processAllergens(list, allergenList)).toEqual(
      jasmine.arrayContaining(['mxmxvkd', 'sqjhc', 'fvjkl'])
    );
  });

  it(`processAllergens for inputs`, () => {
    const list = getFoodList(inputs);
    const allergenList = getAllergenList(list);
    expect(processAllergens(list, allergenList)).toEqual(
      jasmine.arrayContaining([
        'xpbxbv',
        'jtjtrd',
        'fvjkp',
        'xlvrggj',
        'gtqfrp',
        'rlsr',
        'fntg',
        'zhszc',
      ])
    );
  });

  it(`countAllergens for sample`, () => {
    const list = getFoodList(sample);
    const allergenList = getAllergenList(list);
    const badFoods = findIngredientsNotInAllergenList(list, allergenList);
    expect(countAllergens(badFoods, list)).toBe(5);
  });

  it(`countAllergens for input`, () => {
    const list = getFoodList(inputs);
    const allergenList = getAllergenList(list);
    const badFoods = findIngredientsNotInAllergenList(list, allergenList);
    expect(countAllergens(badFoods, list)).toBeGreaterThan(200);
    expect(countAllergens(badFoods, list)).toBeLessThan(2553);
    expect(countAllergens(badFoods, list)).toBeGreaterThan(480);
    expect(countAllergens(badFoods, list)).toBe(2287);
  });
});
