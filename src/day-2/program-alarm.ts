import { Observable, of } from 'rxjs';
import { bufferCount, flatMap, groupBy, map, tap } from 'rxjs/operators';

const fns = {
  add: (x: number, y: number) => x + y,
  multiply: (x: number, y: number) => x * y,
  exit: (x: number, y: number) => 0,
  error: (x: number, y: number) => 1
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
      return fns.error;
      break;
  }
};

const execOp = (
  intCode: [number, number, number, number],
  program: number[]
): number => {
  const [opCode, inputPos1, inputPos2, outputPos] = intCode;
  const inputs = [program[inputPos1], program[inputPos2]];
  return getOpFn(opCode)(inputs[0], inputs[1]);
};

const execGravityAssistProgram = (inputs: number[]): Observable<number[]> => {
  return of(inputs).pipe(
    flatMap(n => n),
    bufferCount(4),
    map(intcode => {
      const [opCode, input1, input2, output] = intcode;
      return getOpFn(opCode);
    }),
    tap(console.log)
  );
};

export { execGravityAssistProgram, fns, getOpFn, execOp };
