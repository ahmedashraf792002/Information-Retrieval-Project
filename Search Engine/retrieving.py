import pandas as pd
# module to read the contents of the file from a csv file
 
from contextlib import redirect_stdout
# module to redirect the output to a text file
from nltk.tokenize import word_tokenize
terms = []
# list to store the terms present in the documents
 
keys = []
# list to store the names of the documents
 
vec_Dic = {}
# dictionary to store the name of the document and the boolean vector as list
 
dicti = {}
# dictionary to store the name of the document and the terms present in it as a
# vector
 
dummy_List = []
# list for performing some operations and clearing them
def tokenize(document):
    '''
    flage==1 mean tokenize using word_tokenize
    flage==0 mean tokenize using split
    document input doctument text
    '''
    return word_tokenize(document)
def filter(documents, rows, cols):
    ''' create a dictionary which has the name of the document as key and the terms present in
    it as the list of strings  which is the value of the key'''
 
    for i in range(rows):
        for j in range(cols):
            # traversal through the data frame
 
            if(j == 1):
                # first column has the name of the document in the csv file
                keys.append(documents.iloc[i]['doc id'])
                #iat [] method is used to return data in a dataframe at the passed location.
                #loc[]accesses a group of rows and columns by label(s) or a boolean array
            else:
                for term in tokenize(documents.iloc[i,j]):
                    dummy_List.append(term)
                # dummy list to update the terms in the dictionary
                    if term not in terms:
                        # add the terms to the list if it is not present else continue
                        terms.append(term)
 
        copy = dummy_List.copy()
        # copying the dummy list to a different list
 
        dicti.update({documents.iloc[i]['doc id']: copy})
        # adding the key value pair to a dictionary
 
        dummy_List.clear()
        # clearing the dummy list
def bool_Representation(dicti, rows, cols):
    '''In this function we get a boolean representation of the terms present in the
    documents in the form of lists'''
 
    terms.sort()
    # we sort the elements in the alphabetical order for the convience
 
    for i in (dicti):
        # for every document in the dictionary we check for each string present in
        # the list
 
        for j in terms:
            # if the string is present in the list we append 1 else we append 0
 
            if j in dicti[i]:
                dummy_List.append(1)
            else:
                dummy_List.append(0)
            # appending 1 or 0 for obtaining the boolean representation
 
        copy = dummy_List.copy()
        # copying the dummy list to a different list
 
        vec_Dic.update({i: copy})
        # adding the key value pair to a dictionary
 
        dummy_List.clear()
        # clearing the dummy list

def Prediction2(query,documents):
    query = query.split()
    frist= documents[query[0]]
    for i in range(1,len(query)):
        #frist = frist & df[query[i]]
        print(query[i])
    return frist
def query_Vector(query):
    '''In this function we represent the query in the form of boolean vector'''
 
    qvect = []
    # query vector which is returned at the end of the function
 
    for i in terms:
        # if the word present in the list of terms is also present in the query
        # then append 1 else append 0
 
        if i in query:
            qvect.append(1)
        else:
            qvect.append(0)
 
    return qvect
    # return the query vector which is obtained in the boolean form
def prediction(q_Vect):
    '''In this function we make the prediction regarding which document is related
    to the given query by performing the boolean operations'''
 
    dictionary = {}
    listi = []
    count = 0
    # initialisation of the dictionary , list and a variable which is further
    # required for performing the computation
 
    term_Len = len(terms)
    # number of terms present in the term list
 
    for i in vec_Dic:
        # for every document in the dictionary containing the terms present in it
        # the form of boolean vector
 
        for t in range(term_Len):
            if(q_Vect[t] == vec_Dic[i][t]):
                # if the words present in the query is also present in the
                # document or if the words present in the query is also absent in
                # the document
                if vec_Dic[i][t] ==1:
                    count += 1
                # increase the value of count variable by one
                # the condition in which words present in document and absent in
                #query , present in query and absent in document is not considered
        if count>0:
            dictionary.update({i: count})
        # dictionary updation here the name of the document is the key and the
        # count variable computed earlier is the value
 
        count = 0
        # reinitialisaion of count variable to 0
    with open('output.txt', 'w') as f:
        with redirect_stdout(f):
            # to redirect the output to a text file
            print("ranking of the documents")
            sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
            for x,i in enumerate(sorted_dict):
                print(i[0], f"is {x+1} relevant document for the given query")
                listi.append(i[0])
    listi.reverse()
    return listi
def main(query):
    #documents = pandas.read_csv(r'docs.csv')
    # to read the data from the csv file as a dataframe
    documents = pd.read_csv("D:\Taskes\IR\Final Project\documents.csv",usecols=[1,2])
    rows = len(documents)
    # to get the number of rows
 
    cols = len(documents.columns)
    # to get the number of columns
 
    filter(documents, rows, cols)
    # function call to read and separate the name of the documents and the terms
    # present in it to a separate list  from the data frame and also create a
    # dictionary which has the name of the document as key and the terms present in
    # it as the list of strings  which is the value of the key
 
    bool_Representation(dicti, rows, cols)
    df = pd.DataFrame(vec_Dic).transpose()
    df.columns= terms
    # In this function we get a boolean representation of the terms present in the
    # documents in the form of lists, later we create a dictionary which contains
    # the name of the documents as key and value as the list of boolean values
    #representing the terms present in the document
    # to get the query input from the user, the below input is given for obtaining
    # the output as in output.txt file
    # hockey is a national sport
 
    query = query.split(' ')
    # splitting the query as a list of strings
    return prediction(query_Vector(query))
