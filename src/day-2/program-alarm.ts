import { EMPTY, Observable, of } from 'rxjs';
import {
  bufferCount,
  filter,
  flatMap,
  groupBy,
  map,
  mergeMap,
  switchMap,
  takeWhile,
  tap,
  toArray,
} from 'rxjs/operators';

const fns = {
  add: (x: number, y: number) => x + y,
  multiply: (x: number, y: number) => x * y,
  exit: (x: number, y: number) => null,
};

const getOpFn = (opCode: number) => {
  switch (opCode) {
    case 1:
      return fns.add;
      break;
    case 2:
      return fns.multiply;
      break;
    case 99:
      return fns.exit;
      break;
    default:
      return () => {
        throw new Error(`unknown op code '${opCode}'`);
      };
      break;
  }
};

const execOp = (intCode: number[], program: number[]): number | null => {
  const [opCode, inputPos1, inputPos2, outputPos] = intCode;
  const inputs = [program[inputPos1], program[inputPos2]];
  return getOpFn(opCode)(inputs[0], inputs[1]);
};

const execGravityAssistProgram$ = (inputs: number[]): Observable<number[]> => {
  const output = [...inputs];
  return of(output).pipe(
    mergeMap((n) => n),
    bufferCount(4),
    map((intcode) => {
      if (intcode.length === 4) {
        const [opCode, input1Pos, input2Pos, outputPos] = intcode;
        const calcOutput = execOp(intcode, output);
        if (calcOutput) {
          output.splice(outputPos, 1, calcOutput);
        }
      }
      return output;
    })
    // toArray(),
    // tap(console.log)
  );
};

export { execGravityAssistProgram$, fns, getOpFn, execOp };
