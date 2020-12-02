const sortNumbers = (values: number[]) => values.sort((a, b) => a - b);
const getHalves = (values: number[]): [number[], number[]] => {
  const half = Math.ceil(values.length / 2);
  return [values.splice(0, half), values.splice(-half)];
};

const getExpensesTo2020 = (expenses: number[]): number[] => {
  const nums = sortNumbers(expenses);
  const [leftHalf, rightHalf] = getHalves(nums);
  let results: number[] = [];
  const sortedRightHalf = rightHalf.reverse();

  leftHalf.map(lv1 => {
    for (const lv of leftHalf) {
      if (lv1 + lv === 2020) {
        results = [lv, lv1];
        break;
      }
    }
  });

  sortedRightHalf.map(rv => {
    for (const lv of leftHalf) {
      if (rv + lv === 2020) {
        results = [lv, rv];
        break;
      }
    }
  });
  return results;
};

export { getExpensesTo2020 };
