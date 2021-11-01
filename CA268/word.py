#!/usr/bin/env python3

def get_plural(s):

    es = ["ch", "sh", "x", "s", "z"]

    vowels = ["a", "e", "i", "o", "u"]

    second = s[-2:]

    first = s[-1]

    word_one = s[:-2]

    word_two = s[:-1]

    if second in es:

        return s + "es"

    elif first in es or first == "o":

        return s + "es"

    elif s[-2] not in vowels and first == "y":

        return word_two + "ies"

    elif first == "f":

        return word_two + "ves"

    elif second == "fe":

        return word_one + "ves"

    else:

        return s + "s"
