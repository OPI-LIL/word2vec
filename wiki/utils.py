import getopt
import sys

from itertools import islice


def parse_args(argv):
    dict = {'limit': None, 'output': "articles.txt"}

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
