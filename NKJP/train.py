import sys
import logging
import os.path
import multiprocessing

from gensim.models import Word2Vec
from NKJP.NKJPSentences import NKJPSentences
from utils import parse_args, slice

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])

    logger = logging.getLogger(program)
    logging.basicConfig(
        filename='nkjp_log.txt',
        format='%(asctime)s: %(levelname)s: %(message)s',
        level=logging.INFO)

    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    args = parse_args(sys.argv[1:])

    for arg in ['input', 'output']:
        if not arg in args:
            logger.error('Argument ' + arg + ' is missing')
            sys.exit(1)

    # check and process input arguments
    inp, outp, limit = args['input'], args['output'], args['limit']

    sentences = slice(NKJPSentences(inp), limit)

    model = Word2Vec(sentences, size=400, window=5, min_count=5, workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use(much) less RAM
    model.init_sims(replace=True)
    model.save(outp)
