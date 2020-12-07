import { countBy, flatten, toLower } from 'ramda';

const countForGroup = (groupAnswers: string[][]): Set<string> =>
  new Set(flatten(groupAnswers));

const totalYessesForGroup = (groups: string[][][]) =>
  groups.reduce((acc, c) => (acc += countForGroup(c).size), 0);

const countAllYessesForGroup = (
  groupAnswers: string[][]
): { [key: string]: number } => countBy(toLower, flatten(groupAnswers));

const totalAllYessesForGroup = (
  numOfPeople: number,
  groupAnswers: string[][]
) =>
  Array.from(
    new Map(Object.entries(countAllYessesForGroup(groupAnswers)))
  ).filter(([_, val]) => val === numOfPeople);

const totalAllYessesForAllGroups = (groups: string[][][]) =>
  groups.reduce(
    (acc, c) => (acc += totalAllYessesForGroup(c.length, c).length),
    0
  );

export {
  countForGroup,
  totalYessesForGroup,
  countAllYessesForGroup,
  totalAllYessesForGroup,
  totalAllYessesForAllGroups,
};
