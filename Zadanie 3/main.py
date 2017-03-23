import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from TType import TType

if __name__ == '__main__':

    # Clas TType introduced, that stores types of outputs from operators
    # Once we parse the input file we do not print output tree

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)\
    # we do not print the tree, as it would not properly generate from an invalid input
    # print(ast)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    print "Type checking finished"