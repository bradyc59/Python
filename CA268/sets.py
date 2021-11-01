#!/usr/bin/env python3

import sys

def unique_list(lst):
    output = []
    for x in lst:
        if x not in output:
            output.append(x)
    return output