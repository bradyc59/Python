#!/usr/bin/env python3

print("Enter numbers (-1 to end): ", end="")
num = int(input())

x = []
y = []

while num != -1:
   if num in x:
      y.append(num)
   x.append(num)
   num = int(input())

for v in y:
   print(str(v) + " ", end="")

print()
