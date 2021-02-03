# Monster Messages

```
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
```

```typescript
const rules = new Map();
const rule4 = equals('a');
const rule5 = equals('b');
const rule3 = (msg) => any( all(zip([rule4, rule5], msg.split(''))), all(zip([rule5, rule4], msg.split('))) );

rules.set(0, rule0);
rules.set(1, rule1);
rules.set(2,rule2);
rules.set(3, rule3);
rules.set(4, rule4);
rules.set(5, rule4);

console.log(rules);
```

Dealing with length

aaaabbb

rule 0: 4 1 5

aaaabbb -> rule 4 = aaabbb
aaabbb -> rule 1 -> rule 2,3 or 3,2 = bb
bb -> rule 5 = b remaining, so invalid

aaaabb -> rule 4 = aaabb
aaabb -> rule 1 -> rule 2,3 or 3,2 = b
b -> rule 5 = valid

## Regex

1: (?:(?:aa|bb)(?:ab|ba))?
2: (?:aa|bb)
3: (?:ab|ba)
