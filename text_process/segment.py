import re
import string
from typing import Generator
from zhon.hanzi import punctuation
import jieba

class Custom_segment:
    def __init__(self):
        self.stopwords = self.get_stopwords()

    def get_stopwords(self):
        with open('baidu_stopwords.txt','r', encoding='utf-8') as f:
            content = f.readlines()
            stopwords = list(map(str.strip, content))
        return  stopwords

    @staticmethod
    def cut_paragraph(text: str) -> Generator:
        '''通过句子结束符号或者换行符加空格进行分段'''
        pattern0 = r'(\.[ "]\n|\![ "]\n|\?[ "]\n'
        pattern1 = r'|。[”]*\n|[！!][”]*\n|[？?][”]*\n|\.{6}[”]*\n[”]*\n|\n\ )'
        pattern = pattern0 + pattern1
        paragraphs_seg = re.split(pattern, text)
        paragraphs = paragraphs_seg[0::2]
        seg = paragraphs_seg[1::2] + [""]
        for s, symbol in zip(paragraphs, seg):
            res = "".join([s, symbol])
            if res:
                yield res

    @staticmethod
    def cut_sentence(text: str) -> Generator:
        pattern = r'(\.[ "]|\![ "]|\?[ "]|。[”]*|！[”]*|？[”]*|\.{6}[”]*)'
        sents_seg = re.split(pattern, text)
        sents = sents_seg[0::2]
        seg = sents_seg[1::2] + [""]
        for s, symbol in zip(sents, seg):
            res = "".join([s, symbol])
            if res:
                yield res

    def tokenizer(self, sent):
        segs = jieba.cut(sent, cut_all=False)
        rem_p_segments = self.remove_punctuation(segs)
        rem_sw_segments = self.del_stopwords(rem_p_segments)
        return list(rem_sw_segments)

    def remove_punctuation(self, words):
        new_words = (word for word in words if word not in punctuation and word not in string.punctuation)
        return new_words     

    def del_stopwords(self, words):
        new_words = (word for word in words if word not in self.stopwords)
        return new_words

