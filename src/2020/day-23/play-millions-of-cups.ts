import { getInputForAMillionCups, playCups, playCupsPartII } from './challenge';
import { inputs, sample } from './inputs';

const millionCupsSample = getInputForAMillionCups(sample).map((v) =>
  v.toString()
);

const millionCupsInput = getInputForAMillionCups(inputs).map((v) =>
  v.toString()
);

console.log('Running: ', process.env.DEBUG);

console.log(`sample, 100: `, playCupsPartII(sample, 100)); // [6,7]
console.log(`sample, 10000000: `, playCupsPartII(millionCupsSample, 10000000)); // [ 934001, 159792 ]
console.log(`inputs, 100: `, playCupsPartII(inputs, 100)); // [ 4,5 ]
console.log(`inputs, 10000000: `, playCupsPartII(millionCupsInput, 10000000)); // [ 931248, 119281 ]

export {};
