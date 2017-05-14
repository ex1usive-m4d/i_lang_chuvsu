import sys

from lexer import *
from parser import *

str = "wor = 2+2 \n var = wor"


def usage():
    sys.stderr.write('Usage: main filename\n')
    sys.exit(1)


str = "var = 2 + 2 \nvar2 = PI + var writec"
# if len(sys.argv) != 2:
#     usage()
filename = "/Users/ivan.bolsakov/PycharmProjects/i_lang/program.ibolshakov"  # sys.argv[1]
str = open(filename).read()
# print str
m = Lexer()
m.Lexer(str)
tokens = m.tokenize()
for token in tokens:
    print token

statements = Parser(tokens).parse()
for statement in statements:
    print statement
    statement.execute()
