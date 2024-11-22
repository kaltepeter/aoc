import { ChildProcess, fork } from 'child_process';
import * as cliProgress from 'cli-progress';
import { exit } from 'process';
import { Instruction, Program } from './challenge';
import { inputs as program } from './inputs';
import assert from 'node:assert';

let nops: number[] = [];
const tasks: Program[] = [];
const maxProcess = 100;

interface IResultRun {
  acc: number;
  success: boolean;
}

program.forEach((l, i) => {
  if (l.command === Instruction.NOP) {
    nops = [...nops, i];
  }
});

let jmps: number[] = [];
program.forEach((l, i) => {
  if (l.command === Instruction.JMP) {
    jmps = [...jmps, i];
  }
});

nops.forEach((n) => {
  const data = [...program];
  data[n] = { ...data[n], command: Instruction.JMP };
  tasks.push(data);
});

jmps.forEach((n) => {
  const data = [...program];
  data[n] = { ...data[n], command: Instruction.NOP };
  tasks.push(data);
});

const totalTasks = nops.length + jmps.length;
const pBar = new cliProgress.SingleBar(
  {
    format: `Run Programs | {bar} | {value}/{total} Programs || ETA: {eta_formatted} || duration: {duration_formatted} || result: {acc}, {success}`,
    hideCursor: true,
  },
  cliProgress.Presets.rect
);
pBar.start(totalTasks, 0);
let processes: ChildProcess[] = [];

const defferred = (data: Program): Promise<[number, boolean]> =>
  new Promise((res, rej) => {
    const compute = fork(__dirname + '/run-program.ts', {
      stdio: ['inherit', 'inherit', 'inherit', 'ipc'],
      detached: true,
    });
    processes.push(compute);
    compute.send(data);
    compute.on('message', (sum: [number, boolean]) => {
      pBar.increment({
        acc: sum[0],
        success: sum[1],
      });
      if (sum[1] === true) {
        return res(sum);
      } else {
        return rej(new Error(`Failed with sum ${sum.toString()}`));
      }
    });

    compute.on('exit', (code, _signal) => {
      if (code !== 0) {
        console.error(`Exit code ${code} for ${compute.pid}`);
        exit(1);
      }
    });
  });

const run = async () => {
  let left = [...tasks];
  const res: { acc: number; success: boolean }[] = [];

  const takeFromQueue = async (): Promise<IResultRun> => {
    if (left.length > 0) {
      const task = left.pop();
      if (task) {
        const p = defferred(task);
        return p
          .then(([acc, success]) => {
            res.push({
              acc,
              success,
            });
            return Promise.resolve({ acc, success });
          })
          .then((r: IResultRun) => {
            processes = [];
            left = []; // need to short circuit
            return Promise.resolve(r);
          })
          .catch(([acc, success]: [number, boolean]) => {
            res.push({
              acc,
              success,
            });
            return takeFromQueue();
          });
      } else {
        return Promise.reject(new Error(`Task is undefined.`));
      }
    } else {
      const lastItem = res[-1];
      return Promise.resolve(lastItem);
    }
  };

  const wait = [];
  // kick off initial wait
  // heavily referenced from: https://github.com/nrwl/nx/blob/2824794a92913624e59d00201ef5dfa936f842fe/packages/workspace/src/tasks-runner/task-orchestrator.ts
  for (let i = 0; i < maxProcess; ++i) {
    const t = takeFromQueue();
    wait.push(t);
  }
  try {
    const result = await Promise.any(wait);
    pBar.stop();
    assert(
      result.acc === 1033,
      `Expected 1033, but got ${JSON.stringify(result)}`
    );
    console.log(`Found result: `, result);
    return result;
  } catch (e) {
    if (e instanceof Error) {
      console.error(`Infinite loop detected. `, e.message);
    } else {
      console.error('Unknown error', e);
    }
  }
};
process.addListener('SIGINT', () => {
  processes.forEach((p) => {
    p.kill('SIGINT');
  });
  process.exit();
});

run().catch((error) => {
  console.error('Error running the program:', error);
});
