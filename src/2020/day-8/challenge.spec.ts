import { execProgram, Instruction, runProgram } from './challenge';
import { inputs, sampleData } from './inputs';
describe(`day 8: Handheld Halting`, () => {
  test(`processSample`, () => {
    expect(sampleData).toEqual([
      { command: Instruction.NOP, value: '+0' },
      { command: Instruction.ACC, value: '+1' },
      { command: Instruction.JMP, value: '+4' },
      { command: Instruction.ACC, value: '+3' },
      { command: Instruction.JMP, value: '-3' },
      { command: Instruction.ACC, value: '-99' },
      { command: Instruction.ACC, value: '+1' },
      { command: Instruction.JMP, value: '-4' },
      { command: Instruction.ACC, value: '+6' },
    ]);
  });

  test(`NOP`, () => {
    expect(execProgram[Instruction.NOP]()).toBe(1);
  });

  test(`ACC increase`, () => {
    let acc = 4;
    acc += execProgram[Instruction.ACC]('+20');
    expect(acc).toBe(24);
  });

  test(`ACC decrease`, () => {
    let acc = 4;
    acc += execProgram[Instruction.ACC]('-20');
    expect(acc).toBe(-16);
  });

  test(`JMP increase`, () => {
    let pos = 3;
    pos += execProgram[Instruction.JMP]('+20');
    expect(pos).toBe(23);
  });

  test(`JMP decrease`, () => {
    let pos = 3;
    pos += execProgram[Instruction.JMP]('-20');
    expect(pos).toBe(-17);
  });

  test(`sampleData`, () => {
    expect(runProgram(sampleData)).toBe(5);
  });

  test(`inputs`, () => {
    expect(runProgram(inputs)).toBe(1317);
  });
});
