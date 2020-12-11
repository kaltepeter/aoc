enum Instruction {
  ACC = 'acc',
  NOP = 'nop',
  JMP = 'jmp',
}

// tslint:disable-next-line: interface-name
interface ProgramLine {
  command: Instruction;
  value: string;
}

type Program = ProgramLine[];

const execProgram = {
  [Instruction.NOP]: () => 1,
  [Instruction.ACC]: (val: string) => {
    const num = +val;
    return num;
  },
  [Instruction.JMP]: (val: string) => {
    const num = +val;
    return num;
  },
};

const runProgram = (program: Program): [number, boolean] => {
  const seenIds: Set<number> = new Set();
  let acc = 0;
  let pos = 0;
  let isFixed = false;
  do {
    if (pos >= program.length) {
      isFixed = true;
      break;
    }
    const { command, value } = program[pos];
    seenIds.add(pos);
    switch (command) {
      case Instruction.ACC:
        acc += execProgram[command](value);
        pos += 1;
        continue;
      case Instruction.JMP:
        pos += execProgram[command](value);
        continue;
      case Instruction.NOP:
        pos += execProgram[command]();
        continue;
      default:
        console.error(`No instructions`);
    }
  } while (seenIds.has(pos) === false);

  // console.log(`FOUND: ${acc} at ${pos}`);
  return [acc, isFixed];
};

const fixProgram = (program: Program) => {
  let acc = 0;
  let nops: number[] = [];
  let isFixed = false;

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

  while (isFixed === false) {
    nops.forEach((n) => {
      let data = [...program];
      data[n] = { ...data[n], command: Instruction.JMP };
      const res = runProgram(data);
      isFixed = res[1];
      if (isFixed === true) {
        acc = res[0];
        return;
      }
    });

    jmps.forEach((n) => {
      let data = [...program];
      data[n] = { ...data[n], command: Instruction.NOP };
      const res = runProgram(data);
      isFixed = res[1];
      if (isFixed === true) {
        acc = res[0];
        return;
      }
    });
  }

  return acc;
};

export {
  Instruction,
  runProgram,
  execProgram,
  Program,
  ProgramLine,
  fixProgram,
};
