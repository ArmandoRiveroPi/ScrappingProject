import re


def initial_clean(string):
    # subDic = {
    #     r'\b\(|\+53(\d?)\D+': r'\1',  # the Cuban prefix
    #     r'\b\(|\+34(\d?)\D+': r'\1',  # the Spanish prefix
    #     r'\b\(|\+1(\d?)\D+': r'\1',  # the US prefix
    #     r'\b(uno|UNO)\b': '1',  # Number 1 written with words
    #     r'\b(dos|DOS)\b': '2',  # Number 2 written with words
    #     r'\b(tres|TRES)\b': '3',  # Number 3 written with words
    #     r'\b(cuatro|CUATRO)\b': '4',  # Number 4 written with words
    #     r'\b(cinco|CINCO)\b': '5',  # Number 5 written with words
    #     r'\b(seis|SEIS)\b': '6',  # Number 6 written with words
    #     r'\b(siete|SIETE)\b': '7',  # Number 7 written with words
    #     r'\b(ocho|OCHO)\b': '8',  # Number 8 written with words
    #     r'\b(nueve|NUEVE)\b': '9',  # Number 9 written with words
    #     r'\b(cero|CERO)\b': '0',  # Number 0 written with words
    #     r'[^0-9 +]+': ' ',  # anything but a +, a space or a number
    #     # r'[|*!]+': ' ',  # bad caracters that refuse to go away
    #     r'\s+': ' ',  # all multiple white spaces
    # }
    subs = [
        [r'\b\(|\+53(\d?)\D+', r'\1'],  # the Cuban prefix
        [r'\b\(|\+34(\d?)\D+', r'\1'],  # the Spanish prefix
        [r'\b\(|\+1(\d?)\D+', r'\1'],  # the US prefix
        [r'\b(uno|UNO)\b', '1'],  # Number 1 written with words
        [r'\b(dos|DOS)\b', '2'],  # Number 2 written with words
        [r'\b(tres|TRES)\b', '3'],  # Number 3 written with words
        [r'\b(cuatro|CUATRO)\b', '4'],  # Number 4 written with words
        [r'\b(cinco|CINCO)\b', '5'],  # Number 5 written with words
        [r'\b(seis|SEIS)\b', '6'],  # Number 6 written with words
        [r'\b(siete|SIETE)\b', '7'],  # Number 7 written with words
        [r'\b(ocho|OCHO)\b', '8'],  # Number 8 written with words
        [r'\b(nueve|NUEVE)\b', '9'],  # Number 9 written with words
        [r'\b(cero|CERO)\b', '0'],  # Number 0 written with words
        [r'[^0-9 +]+', ' '],  # anything but a +, a space or a number
        # r'[|*!]+', ' ',  # bad caracters that refuse to go away
        [r'\s+', ' '],  # all multiple white spaces
    ]
    for sub in subs:
        string = re.sub(sub[0], sub[1], string)
    return string


examples = [
    '52*4x8$6?1-98',
]

examples = [initial_clean(ex) for ex in examples]

print(examples)
