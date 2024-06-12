import pandas as pd
from preprocessing_indexing import Arabic_text_preprocessing
def retrieval(query):
    data = pd.read_csv("D:\Taskes\IR\Final Project\inverted index.csv")
    query=Arabic_text_preprocessing(query)
    first = None
    for i in range(len(query)):
        try:
            output = data[data['Term']==query[i]]['Postings Lists'].values
            output = [int(i) for i in output[0].split('-')]
        except:
            output = []
        if len(output)>0:
            if first is None:
                first = set(output)
            else:
                first = first.intersection(output)
    return list(first)