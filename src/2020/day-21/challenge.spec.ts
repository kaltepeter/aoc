import { fromPairs } from 'ramda';
import {
  countAllergens,
  findIngredientsNotInAllergenList,
  getAllergenList,
  getCanonicalDangerousIngredientList,
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
    expect(findIngredientsNotInAllergenList(list)).toEqual(
      expect.arrayContaining(['kfcds', 'nhms', 'sbzzf', 'trh'])
    );
  });

  it(`processAllergens`, () => {
    const list = getFoodList(sample);
    const res = processAllergens(list);
    expect(fromPairs(Array.from(res.entries()))).toEqual(
      expect.objectContaining({
        mxmxvkd: 'dairy',
        sqjhc: 'fish',
        fvjkl: 'soy',
      })
    );
  });

  it(`processAllergens for inputs`, () => {
    const list = getFoodList(inputs);
    const res = processAllergens(list);
    expect(fromPairs(Array.from(res.entries()))).toEqual(
      expect.objectContaining({
        xpbxbv: 'sesame',
        jtjtrd: 'shellfish',
        fvjkp: 'soy',
        xlvrggj: 'fish',
        gtqfrp: 'eggs',
        rlsr: 'peanuts',
        fntg: 'dairy',
        zhszc: 'wheat',
      })
    );
  });

  it(`countAllergens for sample`, () => {
    const list = getFoodList(sample);
    const badFoods = findIngredientsNotInAllergenList(list);
    expect(countAllergens(badFoods, list)).toBe(5);
  });

  it(`countAllergens for input`, () => {
    const list = getFoodList(inputs);
    const badFoods = findIngredientsNotInAllergenList(list);
    expect(countAllergens(badFoods, list)).toBeGreaterThan(200);
    expect(countAllergens(badFoods, list)).toBeLessThan(2553);
    expect(countAllergens(badFoods, list)).toBeGreaterThan(480);
    expect(countAllergens(badFoods, list)).toBe(2287);
  });

  describe(`part II`, () => {
    it(`getCanonicalDangerousIngredientList(sample)`, () => {
      const list = getFoodList(sample);
      const badFoods = processAllergens(list);
      expect(getCanonicalDangerousIngredientList(badFoods)).toEqual(
        'mxmxvkd,sqjhc,fvjkl'
      );
    });

    it(`getCanonicalDangerousIngredientList(inputs)`, () => {
      const list = getFoodList(inputs);
      const badFoods = processAllergens(list);
      expect(getCanonicalDangerousIngredientList(badFoods)).toEqual(
        'fntg,gtqfrp,xlvrggj,rlsr,xpbxbv,jtjtrd,fvjkp,zhszc'
      );
    });
  });
});
