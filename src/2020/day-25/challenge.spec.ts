import { inputs, sample } from './inputs';
import { findLoop, getEncryptionKey } from './challenge';

describe(`Day 25: Combo Breaker`, () => {
  it(`should process data`, () => {
    expect(sample.length).toBe(2);
  });

  it(`should find loop size for key`, () => {
    expect(findLoop(sample[0])).toBe(8);
    expect(findLoop(sample[1])).toBe(11);
  });

  it(`should return encryption key`, () => {
    expect(getEncryptionKey(sample[0], 11)).toBe(14897079);
    expect(getEncryptionKey(sample[1], 8)).toBe(14897079);
  });

  it(`should return encryption key for inputs`, () => {
    const cardLoopSize = findLoop(inputs[0]);
    const doorLoopSize = findLoop(inputs[1]);
    const encryptionKey1 = getEncryptionKey(inputs[0], doorLoopSize);
    const encryptionKey2 = getEncryptionKey(inputs[1], cardLoopSize);
    expect(encryptionKey1).toBe(encryptionKey2);
    expect(encryptionKey1).toBe(181800);
  });
});
