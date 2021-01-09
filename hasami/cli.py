import fileinput
import sys

import hasami


def main():
    for line in fileinput.input():
        for sentence in hasami.segment_sentences(line, strip_whitespace=True):
            print(sentence, file=sys.stdout)


if __name__ == '__main__':
    sys.exit(main())