import { createReadStream, read, readdir } from 'fs';
import { join } from 'path';
import { stdout } from 'process';
import { helloWorld } from './solution';

const solutionDir = join(__dirname, '..', 'tmp', 'solution');

let testCases: string[] = [];

readdir(join(solutionDir, 'input'), (err, files) => {
  if (err) {
    throw err;
  }
  files.forEach((file) => {
    testCases.push(file);
  });
});

describe.each([...testCases])(`helloWorld(%a)`, (file: string) => {
  const readable = createReadStream(join(solutionDir, 'input', file));

  readable.pipe(stdout);
  it(`should return `, () => {
    expect(helloWorld(readable.read())).toBe('expectedValue');
  });
});
