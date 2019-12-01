import { concat, from, of, pipe, range } from 'rxjs';
import { map, tap, toArray } from 'rxjs/operators';
import { inputs } from './inputs';

const fuelNeededForMass = (mass: number) => Math.floor(mass / 3) - 2;
// const totalFuelNeededByMass = (mass: number)

// const numbers = range(0, 40).pipe(
//   concat(of(9.4)),
//   map(num => {
//     console.log(`num: ${num}, value: ${fuelRequired(num)}`);
//   })
// ).subscribe();

const example = (listOfNumsAndExpectedValues: number[][]) =>
  from(listOfNumsAndExpectedValues)
    .pipe(
      map(([num, expected]) => {
        const val = fuelNeededForMass(num);
        const errorMsg = `${val} does NOT equal ${expected}`;
        console.log(`num: ${num}, value: ${val}, expected: ${expected}`);
        console.assert(val === expected, errorMsg, {
          val,
          expected
        });
      })
    )
    .subscribe();

const fuelCounterUpper = (masses: number[]) => {
  return masses.reduce((acc, cur) => (acc += fuelNeededForMass(cur)), 0);
};

export { example, fuelNeededForMass, fuelCounterUpper };
