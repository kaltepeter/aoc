# day 11

## data

```python
MonkeyTest = Tuple[int, int, int]
Monkey = TypedDict(
    "Monkey",
    {"id": int, "starting_itmes": List[int], "operation": str, "test": MonkeyTest},
)
```

## calc

worry_less = floor(worry / 3)

## func/approach

1. iterate over 20 rounds
   1. monkey inspects item
   1. decrease worry
   1. run test
   1. throw item

5.93s user 0.40s system 116% cpu 5.438 total max RSS 235604 // before
5.61s user 0.44s system 117% cpu 5.137 total max RSS 234200 // eval
10.98s user 0.37s system 108% cpu 10.467 total max RSS 119488 // drop fns cache
11.53s user 0.41s system 107% cpu 11.066 total max RSS 132088 // refactor with partial
5.62s user 0.40s system 117% cpu 5.137 total max RSS 234432 // partial plus cache
5.13s user 0.38s system 118% cpu 4.637 total max RSS 186176 // lru_cache plus partial
0.56s user 0.34s system 495% cpu 0.181 total max RSS 23980 // np swap
1.91s user 0.34s system 163% cpu 1.371 total max RSS 23560 // super mod trick, chinese remainder therom
1.16s user 0.34s system 242% cpu 0.618 total max RSS 24484
// super mod + cache
