import { concat, from, of, pipe, range } from 'rxjs';
import { map, tap, toArray } from 'rxjs/operators';

const fuelRequired = (mass: number) => {
  return Math.floor(mass / 3) - 2;
};

// const numbers = range(0, 40).pipe(
//   concat(of(9.4)),
//   map(num => {
//     console.log(`num: ${num}, value: ${fuelRequired(num)}`);
//   })
// ).subscribe();

const vals = [
  [0, 2],
  [12, 2],
  [14, 2],
  [1969, 654],
  [100756, 33583]
];

const numbers = from(vals)
  .pipe(
    map(([num, expected]) => {
      const val = fuelRequired(num);
      const errorMsg = `${val} does NOT equal ${expected}`;
      console.log(`num: ${num}, value: ${val}, expected: ${expected}`);
      console.assert(val === expected, errorMsg, {
        val,
        expected
      });
    })
  )
  .subscribe();
