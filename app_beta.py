import streamlit as st
import json
import pandas as pd
from google_drive_downloader import GoogleDriveDownloader as gdd
import os
import string

def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@st.cache(allow_output_mutation=True)
def cache_df():
    return (pd.read_csv("data/complete_matches.csv"))


def download_files():
    # https://drive.google.com/file/d/12C2SE_LJXRPJCq0gZhjf4-Sq18ZuDWLT/view?usp=sharing
    data_file = "12C2SE_LJXRPJCq0gZhjf4-Sq18ZuDWLT"



    if os.path.exists("data"):
        pass
    else:
        os.mkdir("data")

    #download the csv file
    if os.path.exists("./data/complete_matches.csv"):
        pass
    else:
        gdd.download_file_from_google_drive(file_id=f'{data_file}',
                                    dest_path='./data/complete_matches.csv')


def search(search_terms, df):
    x=0
    sents = df.sentences.tolist()
    similar = df.matches.tolist()
    other = []
    matches = []
    for s in sents:
        out = s.translate(str.maketrans('', '', string.punctuation))
        words = out.split()
        check = any(item in search_terms for item in words)
        if check==True:
            if s not in matches:
                matches.append(s)
            if isinstance(similar[x], str):
                total = similar[x].split("|||")
                for item in total:
                    if item not in matches:
                        check2 = any(word in item for word in search_terms)
                        if check2 == False:
                            other.append(item)

        x=x+1
    return (matches, other)

download_files()
data = cache_df()



st.title("USHMM Oral Testimony Sentence Embedding Search")

search_form = st.sidebar.form("Searching Form")
search_terms = search_form.text_input("Provide a list of search terms separated by commas")
search_button = search_form.form_submit_button("Search Button")






if search_button:
    words = search_terms.split(",")
    clean_searches = []
    for word in words:
        clean_searches.append(word.strip())

    matches, other = search(clean_searches, data)
    st.write("Here is a list of matches that contain one of your search words:")
    st.write(matches)
    st.write("Here is a list of items that matched based on similarity:")
    st.write(other)
