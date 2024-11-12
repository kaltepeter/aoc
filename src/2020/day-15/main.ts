import { playGame } from './challenge';
import { inputs } from './inputs';
import assert from 'node:assert';

// const startNums = process.argv?.slice(2).map((v) => +v);

// console.log(`StartNums: ${startNums}`);

const result = playGame(inputs[0], 30000000);

assert(result === 689, `expected 689, got ${result}`);

console.log(`result: ${result}`);
