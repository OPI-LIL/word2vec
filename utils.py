__author__ = 'stokowiec'
import getopt
import os
import sys
import logging

from itertools import islice


# This class could be imported from a utility module
class LogMixin(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)


def parse_args(argv):
    dict = {'limit': None}

    try:
        opts, args = getopt.getopt(argv, "hl:i:o:", ["limit=", "input=", "output"])
    except getopt.GetoptError:
        print os.path.basename(sys.argv[0]) + '-i <inputfile> -o <outputfile> -l <limit>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print "-h <help> \n-l <limit on sentences> \n-i <inputfile> \n-o <outputfile> \n"
            sys.exit()
        elif opt in ("-l", "--limit"):
            dict['limit'] = int(arg)
        elif opt in ('-i', '--input'):
            dict['input'] = arg
        elif opt in ('-o', '--output'):
            dict['output'] = arg

    return dict


def slice(iterator, limit):
    if limit == None:
        return iterator
    else:
        return islice(iterator, limit)
