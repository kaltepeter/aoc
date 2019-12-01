import {of, from, pipe, range} from 'rxjs';
import {toArray, map, concat} from 'rxjs/operators';

const fuelRequired = (mass: number) => {
  return Math.floor(mass / 3) - 2;
}

// const numbers = range(0, 40).pipe(
//   concat(of(9.4)),
//   map(num => {
//     console.log(`num: ${num}, value: ${fuelRequired(num)}`);
//   })
// ).subscribe();

const vals = [
  [12, 2],
  [14,2],
  [1969, 654],
  [100756, 33583]
  ];

const numbers = from(vals).pipe(
  map(num => {
    console.log(`num: ${num}, value: ${fuelRequired(num)}`)
  })
).subscribe();