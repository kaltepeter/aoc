import { splitEvery } from 'ramda';

const calcExp = (e: string) => {
  let exp = e.replace('(', '').replace(')', '').split(' ');
  let subExp = splitEvery(2, exp.slice(1));
  let val = +exp[0].trim();
  subExp.forEach(([o, v]) => {
    const vNum = +v;
    if (o === '*') {
      val *= vNum;
    } else if (o === '+') {
      val += vNum;
    } else {
      console.error(`unexpected val: ${v}`);
    }
  });
  return val;
};

const processExpression = (expression: string) => {
  let exp = expression.replace(/\(([\d\*\+ ]*)\)/, (v) =>
    calcExp(v).toString()
  );
  do {
    exp = exp.replace(/\(([\d\*\+ ]*)\)/, (v) => calcExp(v).toString());
  } while (exp.includes('('));

  return calcExp(exp);
};

const calcSumOfAnswers = (listOfExpressions: string[]): number => {
  const res = listOfExpressions.reduce(
    (acc, c) => (acc += processExpression(c)),
    0
  );
  return res;
};

export { processExpression, calcSumOfAnswers };
