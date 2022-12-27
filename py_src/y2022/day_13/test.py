a = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
b = [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]

c = [[[]]]
d = [[]]

e = []
f = [3]

print(f"a: {a} b: {b}")


def run(left_list, right_list, res=list()):
    if isinstance(left_list, int) and isinstance(right_list, list):
        left_list = [left_list]
    elif isinstance(right_list, int) and isinstance(left_list, list):
        right_list = [right_list]

    try:
        for left, right in zip(left_list, right_list, strict=True):
            print(f"left: {left} right: {right} res: {left <= right}")
            if isinstance(left, int) and isinstance(right, int):
                res.append(left <= right)
            else:
                run(left, right, res)
    except ValueError:
        if len(left_list) > len(right_list):
            res.append(False)
        else:
            res.append(True)

    return res


print()
print()
print(f"res a -> b: {run(a, b, list())}")
print()
print()
print(f"res c -> d: {run(c, d, list())}")
print()
print()
print(f"res e -> f: {run(e, f, list())}")
