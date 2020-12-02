import { getExpensesTo2020 } from './challenge';
import { inputs } from './inputs';

describe('1: expense report', () => {
  test(`returns 2020`, () => {
    const values = [1721, 979, 366, 299, 675, 1456];
    const expenseItems = getExpensesTo2020(values);
    const total = expenseItems[0] * expenseItems[1];

    expect(expenseItems[0] + expenseItems[1]).toBe(2020);
    expect(total).toBe(514579);
  });

  test(`value of sample data getExpensesTo2020()`, () => {
    const data = [...inputs];
    const expenseItems = getExpensesTo2020(data);
    const total = expenseItems[0] * expenseItems[1];
    expect(expenseItems[0] + expenseItems[1]).toBe(2020);
    expect(total).toBe(658899);
  });

  // test(`returns 2020 for three numbers`, () => {
  //   const values = [1721, 979, 366, 299, 675, 1456];
  //   const expenseItems = getExpensesTo2020(values);
  //   const total = expenseItems[0] * expenseItems[1];

  //   expect(expenseItems[0] + expenseItems[1] + expenseItems[2]).toBe(2020);
  //   expect(total).toBe(241861950);
  // });

  // test(`value of sample data getExpensesTo2020()`, () => {
  //   const data = [...inputs];
  //   const expenseItems = getExpensesTo2020(data);
  //   const total = expenseItems[0] * expenseItems[1];
  //   expect(expenseItems[0] + expenseItems[1]).toBe(2020);
  //   expect(total).toBe(658899);
  // });

  // describe.each([...inputs.slice(0, 3)])(
  //   'value of sample data [0,3] getExpensesTo2020(%i)',
  //   value => {
  //     test(`returns ${getExpensesTo2020(value)}`, () => {
  //       expect(getExpensesTo2020(value)).toBe(getExpensesTo2020(value));
  //     });
  //   }
  // );
});
