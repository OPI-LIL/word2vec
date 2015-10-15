import multiprocessing

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
    dict = {'limit': None, 'size': 500, 'min_count': 5, 'workers': multiprocessing.cpu_count(), }

    try:
        opts, args = getopt.getopt(argv, "hl:w:m:s:i:", ["limit=", "workers=", "min_count=", "size=", "hostIp="])
    except getopt.GetoptError:
        print os.path.basename(sys.argv[0]) + ' -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print "-h <help> \n-l <limit on sentences> \n-w <workers> \n-m <minimal count of words> \n" \
                  "-s <vector size> \n-i<inputfile> \n-o <outputfile> \n"
            sys.exit()
        elif opt in ("-l", "--limit"):
            dict['limit'] = int(arg)
        elif opt in ("-w", "--workers"):
            dict['workers'] = int(arg)
        elif opt in ('-m', '--min'):
            dict['min_count'] = int(arg)
        elif opt in ('-s', '--size'):
            dict['size'] = int(arg)
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