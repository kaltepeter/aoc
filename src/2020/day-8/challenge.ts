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

const runProgram = (program: Program) => {
  const seenIds: Set<number> = new Set();
  let acc = 0;
  let pos = 0;
  do {
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

  console.log(`FOUND: ${acc} at ${pos}`);
  return acc;
};

export { Instruction, runProgram, execProgram, Program, ProgramLine };
