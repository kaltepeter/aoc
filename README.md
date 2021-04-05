# AOC challenges

https://adventofcode.com/

2020 - https://adventofcode.com/2020
2019 - https://adventofcode.com/2019

## Running locally

- Slow tests are skipped, watch for those if modifying a day.
- Super slow tests are run in separate processes, check readme.
- Code is very rough, a great learning experience.

```bash
npx jest 2020/day-19 --watch # run single day
DEBUG=true npx jest 2020/day-19 # run single day for super slow painful tests, add test name filter too, dump to logs
npm run test:watch # watch all
```

### Creating a new Day

Templates directory has a `day-template` dir. Copy that and modify.

- The test is intentionally broken.
- The Inputs parsing is bare minimum. Modify for complex examples.

## Larger lessons learned

1. 2019

   - The learning on top of challenges stalled me out at day 3.
   - RxJS is great for streams of data, seemed appropriate but as I learned later that year and applied in 2020, something like ramda gives me the functional wins when needed.
   - Timing, I tried to snag puzzles on release and lost sleep due to my brain not shutting off. A team mate flipped that and got up early and did very well. When running a local leaderboard the drop is less important.
   - Local leaderboards and team slack is a fun experience.
   - Puzzles highlight areas you are very unfamiliar with. I got frustrated due to my lack of comp sci background. Later I enrolled in a few free classes to beef up the skills I don't have or get to use in professional life. e.g. functional programming classes, algorithms classes, etc.
   - Do the things you know are smart. I know that refactoring is a last step, yet i constantly thought if Part I is clean Part II will be easier. The more clean I made code often the harder part II is, caveat is if you actually know the optimizations needed for part 2. Again, duh.
   - Testing is not required but a balanced approach can make debugging easier. Exceptions are process intensive slow programs.

2. 2020

   - I learned a ton this year by focusing on just the problems.
   - I tried to apply lessons from 2019, I also really aimed for completion rather than points, since that was my biggest failure last year.
   - I thought of 2019 as a complete failure, in hind sight, I learned the right things to get a lot further.
   - I built on this repo from 2019, I jammed it together in 2019, upgraded stuff and cleaned up this year. Less waste on getting results.
   - Don't be afraid to hook up a debugger, extra step but helped in the end.
   - Don't be afraid to start over, there are several examples where my code was bad and non performant and I had to step back for real input because it wouldn't complete.
   - Abstracting functions, makes testing easier but makes recursive and complex puzzles hard. Balance it.
   - Don't be afraid to look for help when stuck, this greatly helped me with my goal. I made a solid attempt or 3 first to understand better.
   - Don't be afraid to skip/cheat/get help on puzzles that suck the life out of you.
   - Take time to make sure final answer runs call right inputs, too many wrong answers due to this.
   - When really stuck, get close and submit wrong answers, try again. Use those answers for negative test assertions. This really helped with difficult to understand directions and checking assumptions.
   - Check assumptions on data types. Array lookups of arrays may work...sometimes.
   - When reaching for help, just because some math guru says it's 'blah,blah,blah', if it's too hard to understand find another path and come back if interested.
   - Applied from 2019: don't stick to the framework/stack of choice for a puzzle if it's not a good tool for the job. It can be great learning to apply someone's c approach in typescript, but there are degrees of success and watch for red flags that it is the wrong tool.
