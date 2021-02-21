import { difference, uniq } from 'ramda';
import { intersect } from 'util/list';

export interface IFoodList {
  ingredients: string[];
  allergens: string[];
}

export type allergenList = Map<string, string[]>;

const getFoodList = (list: string[]): IFoodList[] => {
  return list
    .map((line) =>
      line.split('(').map((part) => part.replace(/[\(\)]|contains/g, '').trim())
    )
    .map((parts) => ({
      ingredients: parts[0]
        .trim()
        .split(' ')
        .map((i) => i.trim()),
      allergens: parts[1]
        .trim()
        .split(',')
        .map((a) => a.trim()),
    }));
};

// get a map of possible unique ingredients for an allergen
const getAllergenList = (list: IFoodList[]) => {
  const aList = new Map<string, string[]>();
  list.forEach((li) => {
    li.allergens.forEach((a) => {
      const prevIngredients = aList.get(a) || [];
      aList.set(a, uniq([...prevIngredients, ...li.ingredients]));
    });
  });
  return aList;
};

const processAllergens = (
  list: IFoodList[],
  aList: allergenList
): Map<string, string> => {
  const badFoods = new Map<string, string>();
  list.forEach((fl, idx) => {
    const newList = [...list];
    newList.splice(idx, 1);
    fl.allergens.forEach((a) => {
      const remainingIngredients = newList
        .filter((fi) => fi.allergens.includes(a))
        .map((i) => i.ingredients);

      // if no compares, use filtered list
      const possibleAllergens =
        remainingIngredients.length === 0
          ? fl.ingredients.filter((i) => !badFoods.has(i))
          : intersect(
              fl.ingredients.filter((i) => !badFoods.has(i)),
              ...remainingIngredients
            );

      if (possibleAllergens.length === 1) {
        badFoods.set(possibleAllergens[0], a);
      }
    });
  });
  return badFoods;
};

const findIngredientsNotInAllergenList = (
  list: IFoodList[],
  aList: allergenList
) => {
  const allIngredients = list.flatMap((f) => f.ingredients);
  const processedAllergenList = uniq(
    Array.from(processAllergens(list, aList).keys())
  );
  return difference(allIngredients, processedAllergenList);
};

const countAllergens = (listOfSafeFoods: string[], foodList: IFoodList[]) => {
  return foodList
    .flatMap((f) => f.ingredients)
    .filter((i) => listOfSafeFoods.includes(i)).length;
};

const getCanonicalDangerousIngredientList = (badFoods: Map<string, string>) => {
  return Array.from(badFoods.entries())
    .sort(([aIng, aAlg], [bIng, bAlg]) => aAlg.localeCompare(bAlg))
    .flatMap(([ing, alg]) => ing)
    .join(',');
};

export {
  getFoodList,
  getAllergenList,
  findIngredientsNotInAllergenList,
  processAllergens,
  countAllergens,
  getCanonicalDangerousIngredientList,
};
