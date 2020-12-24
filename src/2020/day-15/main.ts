// import { playGame } from "./challenge";

import { playGame } from './challenge';

const startNums = process.argv?.slice(2).map((v) => +v);

console.log(`StartNums: ${startNums}`);

playGame(startNums, 3000000);
