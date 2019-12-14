import metapy
import math

class BM25P(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA
    """
    def __init__(self, k1=1.2, b=0.75, delta=1):
        self.k1 = k1
        self.b = b
        self.delta = delta
        super(BM25P, self).__init__()

    def score_one(self, sd):
        idf = math.log2((sd.num_docs + 1) / sd.doc_count)
        numerator = (self.k1 + 1) * sd.doc_term_count
        denominator = self.k1 * ((1 - self.b) + self.b * (sd.doc_size / sd.avg_dl)) + sd.doc_term_count
        return idf * ((numerator / denominator) + self.delta)

class BM25L(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA
    """
    def __init__(self, k1=1.2, b=0.75, delta=1):
        self.k1 = k1
        self.b = b
        self.delta = delta
        super(BM25L, self).__init__()

    def score_one(self, sd):
        idf = math.log2((sd.num_docs + 1) / (sd.doc_count + 0.5))
        ctd = sd.doc_term_count / (1 - self.b + self.b * (sd.doc_size / sd.avg_dl))
        numerator = (self.k1 + 1) * (ctd + self.delta)
        denominator = self.k1 + (ctd + self.delta)
        return idf * (numerator / denominator)