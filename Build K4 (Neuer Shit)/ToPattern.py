# 1 enemy
# 2 self
# 0 not marked
# ? state not specified
#


input = """ 0 1 0
            0 1 0
            0 0 0"""

flag = "00000"

target = """ - - -
            - - -
            - 1 -"""

input = "".join(input.replace("\n",",").split())

index = int("".join(target.split()).index("1"))

i = index // len(input.replace("\n",",").split())
j = index % len(input.replace("\n",",").split()[0])

priority = 0


print(input + ";" + "".join(target.split()) + ";" + str(i) + ";" + str(j) + ";" + flag + ";" + str(priority))