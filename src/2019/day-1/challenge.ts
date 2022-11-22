import { EMPTY, from, of } from 'rxjs';
import { expand, filter, map, mergeMap, reduce } from 'rxjs/operators';

const fuelNeededForMass = (mass: number) => Math.floor(mass / 3) - 2;
const totalFuelNeededByMass$ = (mass: number) =>
  of(mass).pipe(
    map((m: number) => fuelNeededForMass(m)),
    filter((m: number) => m > 0),
    expand((m: number) =>
      fuelNeededForMass(m) > 0 ? of(fuelNeededForMass(m)) : EMPTY
    ),
    reduce((acc: number, lastMass: number) => (acc += lastMass), 0)
  );

// const numbers = range(0, 40).pipe(
//   concat(of(9.4)),
//   map(num => {
//     console.log(`num: ${num}, value: ${fuelRequired(num)}`);
//   })
// ).subscribe();

const example$ = (listOfNumsAndExpectedValues: number[][]) =>
  from(listOfNumsAndExpectedValues)
    .pipe(
      map(([num, expected]) => {
        const val = fuelNeededForMass(num);
        const errorMsg = `${val} does NOT equal ${expected}`;
        console.log(`num: ${num}, value: ${val}, expected: ${expected}`);
        console.assert(val === expected, errorMsg, {
          val,
          expected,
        });
      })
    )
    .subscribe();

const fuelCounterUpper = (masses: number[]) =>
  masses.reduce((acc, cur) => (acc += fuelNeededForMass(cur)), 0);

const doubleCheckedFuelCounterUpper$ = (masses: number[]) =>
  from(masses).pipe(
    mergeMap((value) => totalFuelNeededByMass$(value)),
    reduce((acc: number, n: number) => (acc += n), 0)
  );

export {
  example$,
  fuelNeededForMass,
  fuelCounterUpper,
  totalFuelNeededByMass$,
  doubleCheckedFuelCounterUpper$,
};
