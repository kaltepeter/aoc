import { inputs as day2Inputs } from './day-2/inputs';
import { checkCrossedWires } from './day-3/crossed-wires';

const day1Vals = [
  [0, 2],
  [12, 2],
  [14, 2],
  [1969, 654],
  [100756, 33583],
];

// day1Example$(day1Vals);
// console.log(`fuelCounterUpper: ${fuelCounterUpper(inputs)}`);
// doubleCheckedFuelCounterUpper$([14, 1969, 100756]).subscribe(v =>
//   console.log(`doubleCheckedFuelCounterUpper: ${v}`)
// );
console.log('');
// execGravityAssistProgram$([...day2Inputs])
//   .pipe(last())
//   .subscribe(v => {
//     console.log(`execGravityAssistProgram$: ${v}`);
//   });
console.log('');
const day2Vals = [...day2Inputs];
const vars = [...Array(100).keys()];
// console.log(vars);
// vars.forEach(noun => {
//   const testVals = [...day2Vals];
//   testVals.splice(1, 1, noun);
//   vars.forEach(verb => {
//     testVals.splice(2, 1, verb);
//     execGravityAssistProgram$([...testVals])
//       .pipe(last())
//       .subscribe(v => {
//         if (v[0] === 19690720) {
//           const val = 100 * noun + verb;
//           console.warn(
//             `part II to intcode : noun: ${noun} verb: ${verb} answer: ${val}`
//           );
//         }
//       });
//   });
// });

checkCrossedWires();
