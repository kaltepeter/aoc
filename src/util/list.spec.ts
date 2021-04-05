import { intersect } from './list';
describe(`util::list`, () => {
  let list1: string[] = [];
  let list2: string[] = [];
  let additionalLists: string[][] = [];

  beforeEach(() => {
    list1 = ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'];
    list2 = ['trh', 'fvjkl', 'sbzzf', 'mxmxvkd'];
    additionalLists = [
      ['sqjhc', 'fvjkl'],
      ['sqjhc', 'mxmxvkd', 'sbzzf'],
    ];
  });

  describe(`intersect`, () => {
    it(`intersect(list1, list2)`, () => {
      expect(intersect(list1, list2)).toEqual(
        jasmine.arrayContaining(['mxmxvkd'])
      );
    });

    it(`intersect(list1, additionalLists)`, () => {
      expect(intersect(list1, ...additionalLists)).toEqual(
        jasmine.arrayContaining(['sqjhc'])
      );
    });
  });
});
