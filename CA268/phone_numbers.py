#!/usr/bin/env python3

import sys

dic = {}

print('Enter a name and number, or a name and ? to query (!! to exit)')

lines = input()
while lines != '!!':
    name, num = lines.split()

    if name not in dic and num != '?':
        dic[name] = num

    elif name in dic and num != "?":
        dic[name] = num

    elif num == '?' and name in dic:
        print('{} has number {}'.format(name, dic[name]))

    elif num == '?' and name not in dic:
        print('Sorry, there is no ' + name)

    lines = input()

print('Bye')
