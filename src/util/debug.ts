import { writeFileSync } from 'fs';

const writeToLog = (file: string, msg: any) => {
  if (process.env['DEBUG']) {
    writeFileSync(file, '\n' + msg, { flag: 'as' });
  }
};

export { writeToLog };
