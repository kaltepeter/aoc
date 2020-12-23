import { filter } from 'ramda';
const isValidPw = ([min, max, letter, word]: Array<
  string | number
>): boolean => {
  const vals = filter((l) => l === letter, `${word}`.split(''));
  return vals.length >= min && vals.length <= max ? true : false;
};

const newIsValidPw = ([min, max, letter, word]: Array<
  string | number
>): boolean => {
  const w = `${word}`;
  const pos1 = w[+min - 1];
  const pos2 = w[+max - 1];
  const res = [pos1 === letter, pos2 === letter];
  const resIsValid = filter((r) => r === true, res);
  return resIsValid.length === 1 ? true : false;
};

const validPasswords = (validatePasswords: boolean[]): boolean[] =>
  filter((isValid) => isValid === true, validatePasswords);

const processPasswords = (
  listOfPasswords: Array<Array<string | number>>
): boolean[] => {
  const validatePasswords = listOfPasswords.map((pass) => isValidPw(pass));
  return validPasswords(validatePasswords);
};

const newProcessPassword = (
  listOfPasswords: Array<Array<string | number>>
): boolean[] => {
  const validatePasswords = listOfPasswords.map((pass) => newIsValidPw(pass));
  return validPasswords(validatePasswords);
};

export { processPasswords, validPasswords, newProcessPassword };
