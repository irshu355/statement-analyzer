import re
import string
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
import pandas as pd
from enums import Countries
from sklearn.metrics.pairwise import cosine_similarity
from statementutils.statementpatterns import StatementPatterns
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

class Normalization():
   def __init__(self):
      self.stop = stopwords.words('english')
      self.porter = PorterStemmer()
      self.lemmatizer = WordNetLemmatizer() 
      pass

   def do(self, sentence):
      #sentence = self.toLower(sentence)
      sentence = self.removePunctuations(sentence)
      sentence = self.removeApostrophe(sentence)
      sentence = self.removeSingleCharacters(sentence)
      sentence = self.removeStopWords(sentence)
      sentence = self.lemmatizeSentence(sentence)
      return sentence
   
          
   def removeSingleCharacters(self,sentence):
      sent = sentence[0].strip()
      splitted = sent.split()
      new_text = ""
      for w in splitted:
         if len(w) > 1:
            new_text = new_text + " " + w
      return new_text.strip()

   def removePunctuations(self,s):
      stripped = re.sub(r'\W+', ' ', s)
      sentence = np.array([stripped])
      return sentence

   def toLower(self,words):
      return words.lower()

   def removeStopWords(self,sentence):
      new_words = ' '.join([word for word in sentence.split() if word not in (self.stop)])
      return new_words

   def removeApostrophe(self,sentence):
      return np.char.replace(sentence, "'", "")

   def lemmatizeSentence(self, sentence):
    token_words=word_tokenize(sentence)
    token_words
    lemmatize_sentence=[]
    for word in token_words:
        #stem_sentence.append(self.porter.stem(word))
        lemmatize_sentence.append(self.lemmatizer.lemmatize(word).strip())
    return " ".join(lemmatize_sentence)

   