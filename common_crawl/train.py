import sys
import getopt
import gensim

from common_crawl.CassandraSentences import CassandraSentences

# Configure logging
import logging

logging.basicConfig(
    filename='cc_log.txt',
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

def trainModel(args):
    limit = args['limit']
    workers = args['workers']
    min_count = args['min_count']
    size = args['size']
    hostIp = args['hostIp']

    logger.info('Training model with limit ' + str(limit) + ' workers ' + str(workers) + ' and minimum count '
                 + str(min_count) + ' with vector size: ' + str(size))

    # import data from cassandra
    sentences = CassandraSentences(hostIp, 'ngramspace', limit)

    try:
        # train model
        model = gensim.models.Word2Vec(sentences, min_count=min_count, workers=workers, size=size)

        # Save model
        logger.info('Saving model to file')

        model.init_sims(replace=True)
        model.save('/home/1o0ko/models/word2vec' + str(limit))

        logger.info('Model has been saved.')

    except Exception as exc:
        logger.exception('Exception in model training: ' + str(exc))


def parse_args(argv):
    dict = {'limit': None, 'min_count': 5, 'workers': 1, 'size': 100, 'hostIp': '10.20.20.213'}

    try:
        opts, args = getopt.getopt(argv, "hl:w:m:s:i:", ["limit=", "workers=", "min_count=", "size=", "hostIp="])
    except getopt.GetoptError:
        print 'common_cralw.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print "-h <help> \n-l <limit on sentences> \n-w <workers> \n-m <minimal count of words> \n-s <vector size>"
            sys.exit()
        elif opt in ("-l", "--limit"):
            dict['limit'] = int(arg)
        elif opt in ("-w", "--workers"):
            dict['workers'] = int(arg)
        elif opt in ('-m', '--min'):
            dict['min_count'] = int(arg)
        elif opt in ('-s', '--size'):
            dict['size'] = int(arg)
        elif opt in ('-i', '--hostIp'):
            dict['hostIp'] = arg

    return dict


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    trainModel(args)

    logger.info('Done!')
