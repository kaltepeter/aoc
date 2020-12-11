import { runProgram } from './challenge';

process.on('message', (data) => {
  const acc = runProgram(data);
  if (process.send) {
    process.send(acc);
    process.exit(0);
  }
});
