import {
  all,
  fromPairs,
  gte,
  is,
  KeyValuePair,
  lte,
  match,
  where,
} from 'ramda';

export interface IPassport {
  byr: number;
  iyr: number;
  eyr: number;
  hgt: string;
  hcl: string;
  ecl: string;
  pid: string;
  cid?: string;
}

const requiredFields: Array<keyof IPassport> = [
  'byr',
  'iyr',
  'eyr',
  'hgt',
  'hcl',
  'ecl',
  'pid',
];

export const eyeColor = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'];

const processPassports = (batchFile: string): IPassport[] =>
  (batchFile
    .split('\n\n')
    .map(
      (p) =>
        p
          .trim()
          .split(/\s/)
          .filter((field: string) => field.includes(':'))
          .map((field) => {
            const [key, val] = field.split(':');
            const v = key === 'pid' ? val : +val;
            const retVal = v ? v : val;
            return [key, retVal];
          })
          .filter((pair) => pair.length === 2) as Array<
          KeyValuePair<string, string | number>
        >
    )
    .map((pairs) => fromPairs(pairs)) as unknown) as IPassport[];

const validateHeightInInches = (hgt: number) => gte(hgt, 59) && lte(hgt, 76);
const validateHeightInCm = (hgt: number) => gte(hgt, 150) && lte(hgt, 193);

const processHeight = (hgt: string) => {
  if (typeof hgt !== 'string') {
    return false;
  }
  const h = parseInt(hgt, 10);
  if (hgt.includes('in')) {
    return validateHeightInInches(h);
  } else if (hgt.includes('cm')) {
    return validateHeightInCm(h);
  }
};

const isPassportValid = where({
  byr: (byr: number) => gte(byr, 1920) && lte(byr, 2002),
  iyr: (iyr: number) => gte(iyr, 2010) && lte(iyr, 2020),
  eyr: (eyr: number) => gte(eyr, 2020) && lte(eyr, 2030),
  hgt: (hgt: string) => processHeight(hgt),
  hcl: (hcl: string) =>
    is(String, hcl) && match(/#[0-9a-f]{6}/, hcl).length > 0,
  ecl: (ecl: string) => is(String, ecl) && eyeColor.includes(ecl),
  pid: (pid: string) => is(String, pid) && match(/^[0-9]{9}$/, pid).length > 0,
});

const hasAllRequiredFields = (passport: IPassport) =>
  all((f) => !!passport[f], requiredFields);

const getValidPassportCountLax = (passports: IPassport[]): number =>
  passports.filter((p) => hasAllRequiredFields(p)).length;

const getValidPassportCount = (passports: IPassport[]): number =>
  passports
    .filter((p) => hasAllRequiredFields(p))
    .filter((p) => isPassportValid(p)).length;

export {
  processPassports,
  hasAllRequiredFields,
  isPassportValid,
  getValidPassportCountLax,
  getValidPassportCount,
};
