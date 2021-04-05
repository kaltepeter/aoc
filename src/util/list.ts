/**
 * Find the intersection (common in all) for many lists.
 * Ramda supports two lists, not more.
 * @param list1 first list
 * @param list2 second list
 * @param rest additional lists
 */
const intersect = (list1: string[], ...rest: string[][]): string[] => {
  const setB = new Set(...rest.splice(0, 1));
  const res = [...new Set(list1)].filter((x) => setB.has(x));
  return rest?.length > 0 ? intersect(res, ...rest) : res;
};

export { intersect };
