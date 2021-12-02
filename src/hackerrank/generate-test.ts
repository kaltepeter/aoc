import child_process from 'child_process';
import {
  createReadStream,
  createWriteStream,
  openSync,
  read,
  readdir,
  readFile,
} from 'fs';
import { join } from 'path';
import { stdout } from 'process';

const test_dir = join(__dirname, '30-days', 'hello-world');

const solutionDir = join(__dirname, 'tmp', 'solution');
const testFile = join(test_dir, '/solution.ts');

readdir(join(solutionDir, 'input'), (err, files) => {
  if (err) {
    throw err;
  }
  files.forEach((file) => {
    const readable = createReadStream(join(solutionDir, 'input', file));

    readable.pipe(stdout);
    // const subprocess = child_process.spawn(`npx ts-node ${testFile}`, {
    //   stdio: ['pipe', 'pipe', 'inherit'],
    // });

    //   readFile(join(solutionDir, 'input', file), (err, data) => {
    //     if(err) {
    //         throw err;
    //     }
    //    const inputArr = data.toString().split('\n');

    // });
    // subprocess.on('exit', (code: number) => {
    //   process.exit(code);
    // });
  });
});
