 #!/usr/bin/env python3

import sys

def make_map():
	s = input()
	stud, mark = s.split()
	dic = {}
	dic[stud] = mark
	s = input()
	return dic.sorted()