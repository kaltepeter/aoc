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
