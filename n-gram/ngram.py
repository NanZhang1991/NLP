import re
from collections import Counter
import math
from pprint import  pprint
import numpy as np
import pandas as pd

class Ngram:
    def chick(self, text):
        """
        Chick input data type
        """       
        if not isinstance(text, str):
            raise ValueError("input data must be string type")
        return text

    def filer_text(self, text):
        """
        Replace all Non-alphanumeric characters with spaces
        """
        clean_text = text.lower()
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', clean_text).replace('\n','')
        return clean_text

    @classmethod
    def get_ngrams(cls, text, n):
        """
        Get n-grams word group
        Parameters
        ---------
        text: string

        Returns
        ---------
        ngrams: generator

        Raises
        ---------        
        """ 
        text = cls().chick(text)      
        text = cls().filer_text(text)
        tokens = [token for token in text.split(" ") if token != ""]
        if len(tokens) < n:
            n = len(tokens)
        ngrams = zip(*[tokens[i:] for i in range(n)])
        for ngram in ngrams:
            yield " ".join(ngram)



class Tfidf:
    def __init__(self, corpus, ngram):
        self.corpus = corpus
        self.ngram = ngram

    def corpus_ngram(self):
        for text in self.corpus:
            for ngram in Ngram.get_ngrams(text, self.ngram):
                yield ngram

    def doc_frequency(self):
        doc_frequency_dic = {}
        for unique_ngram in set(self.corpus_ngram()):
            for text in self.corpus:
                if unique_ngram in set(Ngram.get_ngrams(text, self.ngram)):
                    doc_frequency_dic[unique_ngram]  = doc_frequency_dic.get(unique_ngram, 0) + 1
        return doc_frequency_dic 

    def frequency_tf(self):
        token_dic = Counter(list(self.corpus_ngram()))
        token_count = [token_dic.get(token) / sum(token_dic.values()) for token in token_dic.keys()]
        token_frequency = dict(token_dic.items())
        tf_dic = dict(zip(token_dic.keys(), token_count))
        return token_frequency, tf_dic

    def idf(self):
        idf_dic = {}
        doc_frequency_dic = self.doc_frequency()
        for unique_ngram in set(self.corpus_ngram()):
            idf_dic[unique_ngram] = math.log(len(self.corpus) / (1 + doc_frequency_dic.get(unique_ngram, 0)))
        return idf_dic

    def tfidf(self):
        tf_dic = self.frequency_tf()[1]
        idf_dic = self.idf()
        tfidf = {}
        for unique_ngram in set(self.corpus_ngram()):
            tfidf[unique_ngram] = tf_dic.get(unique_ngram) * idf_dic.get(unique_ngram)
        # norm = np.sqrt(sum([v**2 for v in tfidf.values()]))
        # tfidf = dict(zip(tfidf.keys(), [v/norm for v in tfidf.values()]))
        return tfidf
    
    def global_vocab(self):
        df = pd.DataFrame([self.doc_frequency(), self.frequency_tf()[0], self.idf(), self.tfidf()])
        df = df.T
        df.columns=['doc_frequency','frequency_tf', 'idf', 'tfidf']
        df.reset_index(inplace=True)
        df.rename(columns={"index":'token'}, inplace=True)
        df.insert(1,'ngram',self.ngram)
        df.sort_values(by=['doc_frequency'], ascending=False, inplace=True)
        df.to_json(path_or_buf='global_vocab.json', orient='records', force_ascii=True)
        return df

class CorpusTokens:
    def __init__(self, data, global_vocab):
        self.data = data
        self.global_vocab = global_vocab

    def text_with_tokens(self, text):
        tokens = [self.global_vocab[self.global_vocab['token']==unique_ngram].to_dict(orient='records')[0] \
                for unique_ngram in set(Ngram.get_ngrams(text, ngram))]
        return tokens

    def __call__(self):
        corpus_tokens = self.data.copy()
        corpus_tokens['token'] = corpus_tokens['body'].apply(self.text_with_tokens)
        corpus_tokens.to_json(path_or_buf='corpus_with_tokens.json', orient='records', force_ascii=True)
        return corpus_tokens

if __name__=="__main__":
    data = pd.read_json('corpus.json')[:10]
    corpus = data['body']
    ngram = 2

    tfidf = Tfidf(corpus, ngram)
    global_vocab = tfidf.global_vocab()
    corpus_tokens = CorpusTokens(data, global_vocab)
    corpus_with_tokens = corpus_tokens()
    print(corpus_with_tokens[:5])
