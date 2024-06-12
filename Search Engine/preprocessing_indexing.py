import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,ISRIStemmer,PorterStemmer,SnowballStemmer
nltk.download('stopwords')
nltk.download('wordnet')
def tokenize(document):
    '''
    flage==1 mean tokenize using word_tokenize
    flage==0 mean tokenize using split
    document input doctument text
    '''
    return word_tokenize(document)
def StopWords_Remove(document_tokenize):
    '''
    flage==1 english document
    flage==0 arabic document
    document_tokenize mean document performed tokenize
    '''
    arabic_stop=set(stopwords.words('arabic'))
    return [i for i in document_tokenize if i not in arabic_stop]   
def Arabic_text_preprocessing(text,flage=3):
    '''
    Flage Number
    1: ISRIStemmer
    2: SnowballStemmer
    3: WordNetLemmatizer
    4: POS
    '''
    text1=text
    #The regular expression [^\w\s] is used to match any character that is not a word character (\w) or a whitespace character (\s).
    text = re.sub(r'[^\w\s]', '',text)
    #splitting sentence into tokens
    text=word_tokenize(text.lower())
    #remove stopwords
    text=StopWords_Remove(text)
    #stemming of each word
    if flage<=3:
        if flage==1:
            stem=ISRIStemmer()
            text=[stem.stem(i) for i in text]
        elif flage==2:
            stem=SnowballStemmer('arabic')
            text=[stem.stem(i) for i in text]
        else:
            #Lemmatizer of each word
            lemmatizer=WordNetLemmatizer()
            text=[lemmatizer.lemmatize(i) for i in text]
    else:
        #part of speech of each word
        text=nltk.pos_tag(text)
    return text
def InvertedIndex(*document):
    '''
    *document: must be dict that name is key and doc text is value
    tokenize_flage: must be 1 word_tokenize or 0 split 
    text_flage: must be 1 english or 0 arabic
    bool_apply_stopword: must be 1 apply or 0 don't apply
    stopword_flage: must be 1 english or 0 arabic
    bool_apply_stemming: must be 1 apply or 0 don't apply
    stemming_flage: must be 1 or 2 or 3 and depends on text_flag arabic or english
    '''
    inverted_index = {}
    inverted_index2 = {}
    terms = set([])
    names = []
    document_t = []
    for doc in document:
        for name, text in doc.items():
            names.append(name)
            processed_text = Arabic_text_preprocessing(text)
            terms.update(processed_text)
            document_t.append(processed_text)

    for term in terms:
        document1 = []
        document2 = []
        for document_m in range(len(names)):
            if term in document_t[document_m]:
                document1.append(names[document_m])
                document2.append(document_m + 1)
        inverted_index[term] = document1
        inverted_index2[term] = [len(set(document2)), ' - '.join([str(num) for num in document2])]
    df = pd.DataFrame(inverted_index2)
    df = df.transpose()
    df.columns = ['Document Frequency', 'Postings Lists']
    df.index.name = 'Term'
    return dict(sorted(inverted_index.items())), df.sort_index()