# 1 enemy
# 2 self
# 0 not marked
# ? state not specified
#


input = """ 0 0
            0 P"""

flag = "00000"

# where to set
target = """x -
            - -"""

input = "".join(input.replace("\n",",").split())

index = int("".join(target.split()).index("x"))


i = index // len(target.replace(" ", "").split("\n")[0])
j = index % len(target.replace(" ", "").split("\n")[0])

priority = 0


print(input + ";" + "".join(target.split()) + ";" + str(i) + ";" + str(j) + ";" + flag + ";" + str(priority))