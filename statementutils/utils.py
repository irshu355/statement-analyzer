import re
import string
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
import pandas as pd
from enums import Countries
from sklearn.metrics.pairwise import cosine_similarity
from statementutils.statementpatterns import StatementPatterns
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


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

def get_matches_df(sparse_matrix, name_vector, top=100):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    
    for index in range(0, sparsecols.size):
        left_side[index] = name_vector[sparserows[index]]
        right_side[index] = name_vector[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
    
    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similairity': similairity})


def create_tokenizer_score(new_series, train_series, tokenizer):
    """
    return the tf idf score of each possible pairs of documents
    Args:
        new_series (pd.Series): new data (To compare against train data)
        train_series (pd.Series): train data (To fit the tf-idf transformer)
    Returns:
        pd.DataFrame
    """

    train_tfidf = tokenizer.fit_transform(train_series)
    new_tfidf = tokenizer.transform(new_series)
    X = pd.DataFrame(cosine_similarity(new_tfidf, train_tfidf), columns=train_series.index)
    X['ix_new'] = new_series.index
    score = pd.melt(
        X,
        id_vars='ix_new',
        var_name='ix_train',
        value_name='score'
    )
    score = score.sort_values(by=['score'],ascending=False)
    return score

def cleanTransDataset(dataset,country):
   cities = '|'.join(StatementPatterns.getStates(country))
   dataset = dataset.apply(lambda x: re.sub(cities,'',x))
   dataset = dataset.apply(lambda x:cleanseDesc(x, country))
   
   return dataset

def cleanseDesc(str, country):
   if country == Countries.malaysia:
      str = re.sub(r'(m\s){,1}(sdn+((\s)+bh+(d)?)?)|(berhad?)$','',str)
      return str
   return str


