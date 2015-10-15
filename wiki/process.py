#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys

from gensim.corpora import WikiCorpus

from common.utils import parse_args, slice


def iterate_with_logging(logger, step, generator, function):
    i = 0
    for item in generator:
        function(item)
        i += 1
        if( i%step   == 0):
            logger.info("Processed: " + str(i) + " items")

    logger.info("Finished Saved " + str(i) + " articles")

if __name__ == '__main__':

    # set up logging
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running: %s" % ' '.join(sys.argv))

    # check and process input arguments
    args = parse_args(sys.argv[1:])

    if not 'input' in args:
        logger.error("No input given!")
        sys.exit(1)

    # get args
    inp, outp, limit = args['input'], args['output'], args['limit']

    # prepare corpus
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    texts = slice(wiki.get_texts(), limit);

    # save this for efficiency
    space = " "
    output = open(outp, 'w')
    iterate_with_logging(logger, 10000, texts,
                 lambda text: output.write(space.join(text) + "\n"))

    output.close()