#!/usr/bin/env python3
#
# module layout is as recommended at
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829

'''Experimental PlantUML class diagram parser and data model generator.

Currently supports only a subset of the PlantUML syntax. Can output a
data model definition in one of several formats.
'''

import getopt
import sys

import plantumlparser

def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])

    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)

    for arg in args:
        process(arg)

def process(file):
    print(plantumlparser.parse(file))
        
if __name__ == "__main__":
    sys.exit(main())
