import { getInputForAMillionCups, playCupsPartII } from './challenge';
import { inputs, sample } from './inputs';
import assert from 'node:assert';

const millionCupsSample = getInputForAMillionCups(sample).map((v) =>
  v.toString()
);

const millionCupsInput = getInputForAMillionCups(inputs).map((v) =>
  v.toString()
);

console.log('Running: ', process.env.DEBUG);

const sampleX100 = playCupsPartII(sample, 100);
assert(
  sampleX100[0] === 6 && sampleX100[1] === 7,
  `expected [6,7], got ${sampleX100.toString()}`
);
console.log(`sample, 100: `, sampleX100); // [6,7]

const sampleX10000000 = playCupsPartII(millionCupsSample, 10000000);
assert(
  sampleX10000000[0] === 934001 && sampleX10000000[1] === 159792,
  `expected [934001,159792], got ${sampleX10000000.toString()}`
);

const sampleX10000000Result = sampleX10000000[0] * sampleX10000000[1];
assert(
  sampleX10000000Result === 149245887792,
  `expected 149245887792, got ${sampleX10000000Result}`
);
console.log(
  `sample, 10000000: `,
  sampleX10000000,
  ` result: ${sampleX10000000Result}`
); // [ 934001, 159792 ]

const inputsX100 = playCupsPartII(inputs, 100);
assert(
  inputsX100[0] === 4 && inputsX100[1] === 5,
  `expected [4,5], got ${inputsX100.toString()}`
);
console.log(`inputs, 100: `, inputsX100); // [ 4,5 ]

const inputsX10000000 = playCupsPartII(millionCupsInput, 10000000);
assert(
  inputsX10000000[0] === 931248 && inputsX10000000[1] === 119281,
  `expected [931248, 119281], got ${inputsX10000000.toString()}`
);

const inputsX10000000Result = inputsX10000000[0] * inputsX10000000[1];
assert(
  inputsX10000000Result === 111080192688,
  `expected 111080192688, got ${inputsX10000000Result}`
);
console.log(
  `inputs, 10000000: `,
  inputsX10000000,
  ` result: ${inputsX10000000Result}`
); // [ 931248, 119281 ]

export {};
