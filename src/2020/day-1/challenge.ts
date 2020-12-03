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

const getThreeExpensesTotal2020 = (expenses: number[], sum: number) => {
  const nums = sortNumbers(expenses);
  for (let i = 0; i < nums.length - 2; i++) {
    let l = i + 1
    let r = nums.length - 1
    while (l < r) {
      if (nums[i] + nums[l] + nums[r] === sum) {
        console.log("🚀 ~ triplet found", nums[i], nums[l], nums[r]);
        return [nums[i], nums[l], nums[r]];
      } else if(nums[i] + nums[l] + nums[r] < sum) {
        l += 1;
      } else {
        r -= 1
      }
    }
  }
  return []
};

export { getExpensesTo2020, getThreeExpensesTotal2020 };
