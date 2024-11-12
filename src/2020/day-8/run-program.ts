import { Program, runProgram } from './challenge';

process.on('message', (data) => {
  const acc = runProgram(data as Program);
  if (process.send) {
    process.send(acc);
    process.exit(0);
  }
});
