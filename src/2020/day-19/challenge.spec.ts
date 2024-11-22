import { processRules, createRulesV2 } from './challenge';
import { sample, inputs, sample2 } from './inputs';

describe(`Day 19: Monster Messages`, () => {
  it(`should process data`, () => {
    expect(sample.rules.size).toBe(6);
    expect(sample.messages.length).toBe(5);
    // inputs
    expect(inputs.rules.size).toBe(129);
    expect(inputs.messages.length).toBe(468);
  });

  it(`processRules()`, () => {
    const rules = createRulesV2(sample2.rules);
    expect(processRules(rules, 0, ['ababbb']).length).toBe(1);
    expect(processRules(rules, 0, ['abbbab']).length).toBe(1);
    expect(processRules(rules, 0, ['bababa']).length).toBe(0);
    expect(processRules(rules, 0, ['aaaabbb']).length).toBe(0);
  });

  it(`processRules(sample2)`, () => {
    const rules = createRulesV2(sample2.rules);
    expect(processRules(rules, 0, sample2.messages).length).toBe(2);
  });

  it(`processRules(inputs)`, () => {
    const rules = createRulesV2(inputs.rules);
    const res = processRules(rules, 0, inputs.messages);
    expect(res.length).toBeLessThan(234);
    expect(res.length).toBeGreaterThan(217);
    // expect(res.length).not.toBe(220);
  });

  it(`createRulesVv2`, () => {
    const rules = createRulesV2(sample2.rules);
    expect(rules.get(5)).toEqual('b');
  });
});
