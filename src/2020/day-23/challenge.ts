// const playCups = (input: string) => {
//   const cups = input.split('');
//   const highest = Math.max(...cups.map((v) => +v));
//   const lowest = Math.min(...cups.map((v) => +v));
//   const newOrder = cups.slice(0);
//   const maxMoves = 10;
//   let currentCup: string;
//   for (let i = 0; i < 10; i++) {
//     console.log(newOrder);
//     const curIdx = i >= input.length ? 0 : i;
//     currentCup = newOrder[curIdx];
//     let nextThree = newOrder.splice(curIdx + 1, 3);
//     if (nextThree.length < 3) {
//       nextThree = [...nextThree, ...newOrder.splice(0, 3 - nextThree.length)];
//     }
//     let destCup = +currentCup - 1;
//     let destIdx = newOrder.findIndex((c) => c === destCup.toString());

//     console.log(`(${currentCup}), ${destCup}, ${curIdx}, ${i}`);
//     do {
//       if (nextThree.includes(destCup.toString())) {
//         destCup = +destCup - 1;
//         // const destIdx = newOrder.findIndex(c => c === destCup.toString());
//         // console.log(destIdx);
//       } else if (destCup < lowest) {
//         destCup = highest;
//         // destIdx = newOrder.findIndex((c) => c === destCup.toString());
//       }
//     } while (nextThree.includes(destCup.toString()) || destCup < lowest);
//     destIdx = newOrder.findIndex((c) => c === destCup.toString());

//     if (newOrder.length < input.length && destIdx < curIdx) {
//       const target = newOrder.splice(0, destIdx + 1);
//       newOrder.splice(newOrder.length, 0, ...target);
//       destIdx = newOrder.findIndex((c) => c === destCup.toString());
//       newOrder.splice(
//         destIdx + 1,
//         0,
//         ...nextThree.splice(0, 3 - target.length)
//       );
//       newOrder.splice(0, 0, ...nextThree);
//     } else {
//       newOrder.splice(destIdx + 1, 0, ...nextThree);
//     }

//     console.log(
//       `nextThree: ${nextThree}, destCup: ${destCup}:${destIdx}, curCup: ${currentCup}`
//     );
//   }
//   if (newOrder.length !== input.length) {
//     console.error('Failed');
//   }
//   const res = newOrder.join('').split('1');
//   return `${res[1]}${res[0]}`;
// };

const playCups = (input: string) => {};

export { playCups };
