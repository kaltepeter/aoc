import fs from 'fs';
import path from 'path';
import {
  getValidPassportCountLax,
  isPassportValid,
  processPassports,
} from './challenge';
import { inputs, invalidPassportsInputs, validPassportsInputs } from './inputs';
const values = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const validPassportsSampleData = validPassportsInputs.map((p) => [
  { ...p },
  true,
]);

const invalidPassportsSampleData = invalidPassportsInputs.map((p) => [
  { ...p },
  false,
]);

describe('4: passport validation', () => {
  test(`returns 2`, () => {
    const passports = processPassports(values);
    const validPassports = getValidPassportCountLax(passports);
    expect(passports.length).toBe(4);
    expect(validPassports).toBe(2);
  });

  test(`returns 206 valid passports`, () => {
    const passports = [...inputs];
    const validPassports = getValidPassportCountLax(passports);
    expect(passports.length).toBe(257);
    expect(validPassports).toBe(206);
  });

  // describe.each([...validPassportsSampleData, ...invalidPassportsSampleData])(
  //   'isPassportValid(%p) is %p',
  //   (value: IPassport, expected: boolean) => {
  //     test(`returns ${expected}`, () => {
  //       const passport = { ...value };
  //       const isValid = isPassportValid(passport);
  //       expect(isValid).toBe(expected);
  //     });
  //   }
  // );

  describe('hcl', () => {
    test(`should validate true for '#123abc'`, () => {
      console.log({ ...validPassportsInputs[0], hcl: '#123abc' });
      expect(
        isPassportValid({ ...validPassportsInputs[0], hcl: '#123abc' })
      ).toBe(true);
    });

    test(`should validate false for '#123abz'`, () => {
      expect(
        isPassportValid({ ...validPassportsInputs[0], hcl: '#123abz' })
      ).toBe(false);
    });
    test(`should validate false for '123abc'`, () => {
      expect(
        isPassportValid({ ...validPassportsInputs[0], hcl: '123abc' })
      ).toBe(false);
    });
  });

  describe('ecl', () => {
    test(`should validate false for 'brn'`, () => {
      expect(isPassportValid({ ...validPassportsInputs[0], ecl: 'brn' })).toBe(
        true
      );
    });

    test(`should validate false for 'wat'`, () => {
      expect(isPassportValid({ ...validPassportsInputs[0], ecl: 'wat' })).toBe(
        false
      );
    });
  });
});
