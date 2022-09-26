import render as rd
import sys

if (len(sys.argv) == 2):
    print(sys.argv[1])
    rd.render(sys.argv[1])