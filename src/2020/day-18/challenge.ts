import { splitEvery } from 'ramda';

const calcExp = (e: string) => {
  const exp = e.replace('(', '').replace(')', '').split(' ');
  const subExp = splitEvery(2, exp.slice(1));
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

const processPlus = (exp: string): string =>
  exp.replace(/(\d+\s\+\s\d+)/, (v) => calcExp(v).toString());

const processPrePlus = (exp: string): string => {
  do {
    exp = exp.replace(/(\d+\s\+\s\d+)/, (v) => calcExp(v).toString());
  } while (exp.includes('+'));
  return exp;
};

const processParens = (exp: string, internalFn?: (v: string) => string) =>
  exp.replace(/\(([\d\*\+ ]*)\)/, (v) => {
    if (internalFn) {
      const preProcess = internalFn(v);
      return calcExp(preProcess).toString();
    } else {
      return calcExp(v).toString();
    }
  });

const processExpression = (expression: string) => {
  let exp = expression;
  do {
    exp = processParens(exp);
  } while (exp.includes('('));

  return calcExp(exp);
};

const processExpressionV2 = (expression: string) => {
  let exp = expression;
  do {
    exp = processParens(exp, processPrePlus);
  } while (exp.includes('('));

  do {
    exp = processPlus(exp);
  } while (exp.includes('+'));

  return calcExp(exp);
};

const calcSumOfAnswers = (
  listOfExpressions: string[],
  processFn: (arg0: string) => number = processExpression
): number => {
  const res = listOfExpressions.reduce((acc, c) => (acc += processFn(c)), 0);
  return res;
};

export { processExpression, calcSumOfAnswers, processExpressionV2 };
