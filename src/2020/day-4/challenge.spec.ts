import fs from 'fs';
import path from 'path';
import {
  getValidPassportCount,
  getValidPassportCountLax,
  IPassport,
  isPassportValid,
  processPassports,
} from './challenge';
import { inputs, invalidPassportsInputs, validPassportsInputs } from './inputs';
const values = fs
  .readFileSync(path.join(__dirname, 'sample-data.txt'))
  .toString('utf-8');

const validPassportsSampleData: Array<
  [IPassport, boolean]
> = validPassportsInputs.map((p) => [{ ...p }, true]);

const invalidPassportsSampleData: Array<
  [IPassport, boolean]
> = invalidPassportsInputs.map((p) => [{ ...p }, false]);

const getValidPassport = () => ({ ...validPassportsInputs[0] });

describe('4: passport validation', () => {
  let validPassport: IPassport;

  beforeEach(() => {
    validPassport = { ...getValidPassport() };
  });
  test(`returns 2 for lax checker`, () => {
    const passports = processPassports(values);
    const validPassports = getValidPassportCountLax(passports);
    expect(passports.length).toBe(4);
    expect(validPassports).toBe(2);
  });

  test(`returns 206 valid passports for lax checker`, () => {
    const passports = [...inputs];
    const validPassports = getValidPassportCountLax(passports);
    expect(passports.length).toBe(257);
    expect(validPassports).toBe(206);
  });

  test(`returns 123 valid passports`, () => {
    const passports = [...inputs];
    const validPassports = getValidPassportCount(passports);
    expect(passports.length).toBe(257);
    expect(validPassports).toBe(123);
  });

  describe.each([...validPassportsSampleData, ...invalidPassportsSampleData])(
    'isPassportValid(%p) is %p',
    (value: IPassport, expected: boolean) => {
      test(`returns ${expected}`, () => {
        const passport = { ...value };
        const isValid = isPassportValid(passport);
        expect(isValid).toBe(expected);
      });
    }
  );

  describe('byr', () => {
    test(`should validate true for '2002'`, () => {
      expect(isPassportValid({ ...validPassport, byr: 2002 })).toBe(true);
    });

    test(`should validate false for '2003'`, () => {
      expect(isPassportValid({ ...validPassport, byr: 2003 })).toBe(false);
    });
  });

  describe('iyr', () => {
    test(`should validate true for '2010'`, () => {
      expect(isPassportValid({ ...validPassport, iyr: 2010 })).toBe(true);
    });

    test(`should validate false for '2009'`, () => {
      expect(isPassportValid({ ...validPassport, iyr: 2009 })).toBe(false);
    });

    test(`should validate false for '2021'`, () => {
      expect(isPassportValid({ ...validPassport, iyr: 2021 })).toBe(false);
    });
  });

  describe('eyr', () => {
    test(`should validate true for '2020'`, () => {
      expect(isPassportValid({ ...validPassport, eyr: 2020 })).toBe(true);
    });

    test(`should validate false for '2019'`, () => {
      expect(isPassportValid({ ...validPassport, eyr: 2019 })).toBe(false);
    });

    test(`should validate false for '20'`, () => {
      expect(isPassportValid({ ...validPassport, eyr: 20 })).toBe(false);
    });

    test(`should validate false for '2031'`, () => {
      expect(isPassportValid({ ...validPassport, eyr: 2031 })).toBe(false);
    });
  });

  describe('hgt', () => {
    test(`should validate true for '60in'`, () => {
      expect(isPassportValid({ ...validPassport, hgt: '60in' })).toBe(true);
    });

    test(`should validate true for '190cm'`, () => {
      expect(isPassportValid({ ...validPassport, hgt: '190cm' })).toBe(true);
    });

    test(`should validate false for '190in'`, () => {
      expect(isPassportValid({ ...validPassport, hgt: '190in' })).toBe(false);
    });

    test(`should validate false for '190'`, () => {
      expect(isPassportValid({ ...validPassport, hgt: '190' })).toBe(false);
    });
  });

  describe('hcl', () => {
    test(`should validate true for '#123abc'`, () => {
      expect(isPassportValid({ ...validPassport, hcl: '#123abc' })).toBe(true);
    });

    test(`should validate false for '#123abz'`, () => {
      expect(isPassportValid({ ...validPassport, hcl: '#123abz' })).toBe(false);
    });
    test(`should validate false for '123abc'`, () => {
      expect(isPassportValid({ ...validPassport, hcl: '123abc' })).toBe(false);
    });
  });

  describe('ecl', () => {
    test(`should validate true for 'brn'`, () => {
      expect(isPassportValid({ ...validPassport, ecl: 'brn' })).toBe(true);
    });

    test(`should validate false for 'wat'`, () => {
      expect(isPassportValid({ ...validPassport, ecl: 'wat' })).toBe(false);
    });
  });

  describe('pid', () => {
    test(`should validate true for '000000001'`, () => {
      expect(isPassportValid({ ...validPassport, pid: '000000001' })).toBe(
        true
      );
    });

    test(`should validate false for '0123456789'`, () => {
      expect(isPassportValid({ ...validPassport, pid: '0123456789' })).toBe(
        false
      );
    });
  });
});
