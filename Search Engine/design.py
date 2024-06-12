import streamlit as st
from retrieving3 import main
from evaluation import get_cosine
import pandas as pd
from preprocessing_indexing import Arabic_text_preprocessing
from Evalution import evaluate

# Define global variables
documents = pd.read_csv("D:\Taskes\IR\Final Project\documents.csv", usecols=[1, 2])
input_query, output_search, relevant = '', '', ''

# List to store downloaded document paths

# Define the function for searching
def search():
    global input_query
    query = st.text_input('Enter your query:')
    input_query = ' '.join(Arabic_text_preprocessing(query)) 
    if st.button('Search'):
        # Perform search operation here (dummy search for now)
        output = perform_search(query)
        # Display search results
        st.write('Search Results:')
        text = 'Document'
        text_output = ' '
        with open('search_results.txt', 'w') as file:
            for result in output:
                file.write(str(result) + '\t')
                # Inside the loop, you open another file
                file_path = f"D:\Taskes\IR\Final Project\documents\{str('document'+str(result))}.txt"  
                with open(file_path, encoding='utf-8') as inner_file:
                    file_bytes = inner_file.read()
                    button=st.download_button(
                    label=f'{text + str(result)}',
                    data=file_bytes,
                    file_name=f"{text+str(result)}.txt",
                    mime="application/octet-stream"
                )

# Define the function for ranking
def ranking():
    if st.button('Rank'):
        # Perform ranking operation here (dummy ranking for now)
        ranked_documents = perform_ranking()
        # Display ranked documents
        top = len(ranked_documents)
        print(top)
        if top > 5:
            top = 5
        with open('ranked_results.txt', 'w') as file:
            for index in range(top):
                file.write(ranked_documents[index][0][8:] + '\t')
                file_path = f"D:\Taskes\IR\Final Project\documents\{str('d'+ranked_documents[index][0][1:])}.txt"  
                with open(file_path, encoding='utf-8') as inner_file:
                    file_bytes = inner_file.read()
                st.download_button(
                    label=ranked_documents[index][0],
                    data=file_bytes,
                    file_name="file.txt",
                    mime="application/octet-stream"
                )

# Define the function for evaluation
def evaluation():
    if st.button('Evaluate'):
        # Perform evaluation operation here (dummy evaluation for now)
        evaluation_results = perform_evaluation()
        # Display evaluation results

# Dummy search function (replace with actual search logic)
def perform_search(query):
    # Dummy search results
    output = main(query)
    return output

def perform_ranking():
    global output_search, documents, input_query
    li = []
    with open('search_results.txt') as file:
        li.append(file.read())
    output_search = li[0].split('\t')[:-1]
    dict = {}
    for i in output_search:
        document = str(list(documents['Documents'][documents['doc id'] == str('document'+i)].values)[0])
        value = get_cosine(document, input_query)
        dict[f'Document{i}'] = value
    dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return dict

# Dummy evaluation function (replace with actual evaluation logic)
def perform_evaluation():
    global output_search, relevant
    li = []
    with open('search_results.txt') as file:
        li.append(file.read())
    output_search = [int(i) for i in li[0].split('\t')[:-1]]
    li = []
    with open('ranked_results.txt') as file:
        li.append(file.read())
    relevant = [int(i) for i in li[0].split('\t')[:-1]]
    print(relevant)
    print(output_search)
    precision, recall, f1 = evaluate(relevant, output_search)
    # Dummy evaluation results
    st.write('Evaluation Results:')
    st.write('Precision :', precision)
    st.write('Recall :', recall)
    st.write('F1 :', f1)

# Streamlit app layout
st.title('Search Engine App')

# Add the search section
st.header('Search Section')
search()

# Add the ranking and evaluation sections side by side
col1, col2 = st.columns(2)
with col1:
    st.header('Ranking Section')
    ranking()
with col2:
    st.header('Evaluation Section')
    evaluation()
