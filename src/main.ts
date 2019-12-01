import {
  doubleCheckedFuelCounterUpper$,
  example$ as day1Example$,
  fuelCounterUpper
} from './day-1/challenge';
import { inputs } from './day-1/inputs';

const day1Vals = [
  [0, 2],
  [12, 2],
  [14, 2],
  [1969, 654],
  [100756, 33583]
];

// day1Example$(day1Vals);
console.log(`fuelCounterUpper: ${fuelCounterUpper(inputs)}`);
doubleCheckedFuelCounterUpper$([14, 1969, 100756]).subscribe(v =>
  console.log(`doubleCheckedFuelCounterUpper: ${v}`)
);
