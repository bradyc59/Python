 #!/usr/bin/env python3

import sys

dic = {}

def make_map():
    s = sys.stdin.readlines()
    for line in s:
        stud, mark = line.split()
        dic[stud] = mark
        line = sys.stdin.readline()
        return dic
