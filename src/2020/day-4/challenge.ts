import {
  all,
  fromPairs,
  gte,
  is,
  KeyValuePair,
  lte,
  match,
  propIs,
  propSatisfies,
  where,
  __,
} from 'ramda';

export interface IPassport {
  byr: number;
  iyr: string;
  eyr: string;
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
          .map((field) => field.split(':'))
          .filter((pair) => pair.length === 2) as Array<
          KeyValuePair<string, string>
        >
    )
    .map((pairs) => fromPairs(pairs)) as unknown) as IPassport[];

const isPassportValid = where({
  byr: propIs(Number) && gte(__, 1920) && lte(__, 2002),
  iyr: propIs(Number) && gte(__, 2010) && lte(__, 2020),
  eyr: propIs(Number) && gte(__, 2020) && lte(__, 2030),
  // hgt: propIs(String) && propSatisfies((x) => x.contains('in')),
  hcl: (hcl: string) =>
    is(String, hcl) && match(/#[0-9a-f]{6}/, hcl).length > 0,
  ecl: propIs(String) && propSatisfies((x: string) => eyeColor.includes(x)),
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
