import { processPasswords, newProcessPassword } from './challenge';
import { inputs } from './inputs';

describe('2: corrupt passwords', () => {
  test(`returns 2`, () => {
    const values = [
      [1, 3, 'a', 'abcde'],
      [1, 3, 'b', 'cdefg'],
      [2, 9, 'c', 'ccccccccc'],
    ];
    const validatePasswords = processPasswords(values);

    expect(validatePasswords.length).toBe(2);
  });

  test(`value of sample data processPasswords()`, () => {
    const data = [...inputs];
    const validatePasswords = processPasswords(data);
    expect(validatePasswords.length).toBe(483);
  });

  test(`returns 1`, () => {
    const values = [
      [1, 3, 'a', 'abcde'],
      [1, 3, 'b', 'cdefg'],
      [2, 9, 'c', 'ccccccccc'],
    ];
    const validatePasswords = newProcessPassword(values);

    expect(validatePasswords.length).toBe(1);
  });

  test(`value of sample data newProcessPassword()`, () => {
    const data = [...inputs];
    const validatePasswords = newProcessPassword(data);
    expect(validatePasswords.length).toBe(482);
  });
});
