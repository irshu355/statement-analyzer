import re
import string
def hasValue(patterns, text):
   return re.search("(" + ")|(".join(patterns) + ")",text,flags=re.IGNORECASE)

def cleanText(text):
   table = str.maketrans({key: None for key in string.punctuation})
   text = text.translate(table)
   text = ' '.join(text.split())


# everything related to text matching

def ngrams(string, n=10):
    string = re.sub(r'[,-./]|\s',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]