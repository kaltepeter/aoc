import { fork } from 'child_process';
import { exit } from 'process';
import { Instruction, Program } from './challenge';
import { inputs as program } from './inputs';

let nops: number[] = [];
let tasks: Program[] = [];
const maxProcess = 3;

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

const run = (data: Program) => {
  const compute = fork('run-program.ts');
  compute.send(data);
  compute.on('message', (sum: [number, boolean]) => {
    if (sum[1] === true) {
      console.log(`ACC is ${sum[0]}, ${sum[1]}`);
      exit(0);
    }
  });
};

nops.forEach((n) => {
  let data = [...program];
  data[n] = { ...data[n], command: Instruction.JMP };
  tasks.push(data);
});

jmps.forEach((n) => {
  let data = [...program];
  data[n] = { ...data[n], command: Instruction.NOP };
  tasks.push(data);
});

const defferred = (data: Program) =>
  new Promise((res, rej) => {
    const compute = fork('run-program.ts');
    compute.send(data);
    compute.on('message', (sum: [number, boolean]) => {
      if (sum[1] === true) {
        console.log(`ACC is ${sum[0]}, ${sum[1]}`);
        res(sum);
      } else {
        rej(sum);
      }
    });
  });

const process = async () => {
  const left = [...tasks];
  const res = [];

  async function takeFromQueue(): Promise<any> {
    if (left.length > 0) {
      const task = left.pop();
      if (task) {
        const p = defferred(task);
        return p
          .then((code) => {
            res.push({
              task,
              success: code === 0,
            });
          })
          .then(takeFromQueue)
          .catch(takeFromQueue);
      }
    } else {
      return Promise.resolve(null);
    }
  }

  const wait = [];
  for (let i = 0; i < maxProcess; ++i) {
    wait.push(takeFromQueue());
  }
  try {
    const result = await Promise.race(wait);
    console.log('🚀 ~ file: main.ts ~ line 90 ~ process ~ result', result);
  } catch (e) {
    console.error(`Infinite loop detected. `, e.message);
  }
};

process();
