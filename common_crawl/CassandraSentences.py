import string

from cassandra.cluster import Cluster


# Logging stuff
from mixins import LogMixin

class CassandraSentences(object, LogMixin):
    def __init__(self, hostIp, table, limit=None):
        self.hostIp = hostIp
        self.table = table
        self.limit = limit

    def __iter__(self):
        from itertools import islice

        sentences = self.fetch(self.hostIp, self.table)

        if self.limit is not None:
            sentences = islice(sentences, self.limit)

        for sentence in sentences:
            yield sentence

    def clean_text(self, text):
        from string import digits
        return text.encode('utf-8', 'ignore').translate(None, string.punctuation + digits).lower()

    def fetch(self, hostIp, table):
        from nltk.tokenize import sent_tokenize, word_tokenize

        try:

            cluster = Cluster(contact_points=[hostIp], protocol_version=2)
            session = cluster.connect(table)
            session.default_timeout = 3600

            rows = session.execute('SELECT key, content FROM text')

            for row in rows:
                for sentence in sent_tokenize(row.content):
                    stripped = self.clean_text(sentence)
                    yield word_tokenize(stripped)

        except Exception as exc:
            self.logger.exception('Unexpected error: ' + str(exc))
            raise