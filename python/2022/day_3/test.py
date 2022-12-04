import string


lower_letters = string.ascii_lowercase[:26]
upper_letters = string.ascii_uppercase[:26]
letters = upper_letters + lower_letters
priorities = [i for i in range(1, 52 + 1)]

print(priorities)
print(lower_letters)
print(upper_letters)

for let in letters:
    letter = ord(let)
    print(f"char of ASCII {let} is {letter}")

print(set("vJrwpWtwJgWrhcsFMMfFFhFp"))
