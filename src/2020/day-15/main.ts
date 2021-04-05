import { playGame } from './challenge';
import { inputs } from './inputs';

// const startNums = process.argv?.slice(2).map((v) => +v);

// console.log(`StartNums: ${startNums}`);

const result = playGame(inputs[0], 30000000);

if (result !== 689) {
  console.error(`FAILED`);
}

console.log(`result: ${result}`);
