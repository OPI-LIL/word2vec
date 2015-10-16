import os
import sys
import logging

from gensim.models import Word2Vec

from common_crawl.CassandraSentences import CassandraSentences
from utils.utils import parse_args

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])

    logger = logging.getLogger(program)
    logging.basicConfig(
        filename='cc_log.txt',
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.DEBUG)

    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    args = parse_args(sys.argv[1:])

    for arg in ['input', 'output']:
        if not arg in args:
            logger.error('Argument ' + arg + ' is missing')
            sys.exit(1)

    limit, workers, min_count, size, input, output = args['limit'], args['workers'], args['min_count'], \
                                                     args['size'], args['input'], args['output']

    # log arguments
    logger.info('Training with: ' + ' '.join([k + " : " + str(v) for k, v in args.iteritems()]))

    # import data from cassandra
    sentences = CassandraSentences(input, 'ngramspace', limit)

    try:
        # train model
        model = Word2Vec(sentences, min_count=min_count, workers=workers, size=size)

        # Save model
        logger.info('Saving model to file')
        model.init_sims(replace=True)

        name = output + "_" + str(limit)

        model.save(name)
        logger.info('Model has been saved as ' + name)

    except Exception as exc:
        logger.exception('Exception in model training: ' + str(exc))

    logger.info('Done!')
