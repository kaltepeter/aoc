import { flatten } from 'ramda';

const countForGroup = (groupAnswers: string[][]): Set<string> =>
  new Set(flatten(groupAnswers));

const totalYessesForGroup = (groups: string[][][]) =>
  groups.reduce((acc, c) => (acc += countForGroup(c).size), 0);

export { countForGroup, totalYessesForGroup };
