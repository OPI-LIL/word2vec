import sys
import logging
import os.path
import gensim
from NKJP.NKJPSentences import NKJPSentences

if __name__ == "__main__":

    srcPath = "D:/DATA/NKJP-PodkorpusMilionowy/"
    fileName = "text.xml"

    program = os.path.basename(sys.argv[0])

    logger = logging.getLogger(program)
    logging.basicConfig(
        fileName="nkjt_log.txt",
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO)

    # Train word2vec on NKJP
    sentences = NKJPSentences(srcPath, fileName)
    model = gensim.models.Word2Vec(sentences, min_count=5)

    model.save('word2vec')
