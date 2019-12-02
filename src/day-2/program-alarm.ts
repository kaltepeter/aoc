import { EMPTY, Observable, of } from 'rxjs';
import { bufferCount, flatMap, groupBy, map, tap } from 'rxjs/operators';

const fns = {
  add: (x: number, y: number) => x + y,
  multiply: (x: number, y: number) => x * y,
  exit: (x: number, y: number) => null
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

const execGravityAssistProgram = (inputs: number[]): Observable<number[]> => {
  const output = [...inputs];
  return of(inputs).pipe(
    flatMap(n => n),
    bufferCount(4),
    map(intcode => {
      const [opCode, input1Pos, input2Pos, outputPos] = intcode;
      const calcOutput = execOp(intcode, output);
      if (calcOutput) {
        output.splice(outputPos, 1, calcOutput);
      }
      // console.log('TCL: val', output, outputPos, calcOutput);
      return output;
    }),
    tap(console.log)
  );
};

export { execGravityAssistProgram, fns, getOpFn, execOp };
