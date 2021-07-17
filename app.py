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

    return (pd.read_csv("data/sentence_data.csv"))

@st.cache(allow_output_mutation=True)
def cache_paras():
    return (pd.read_csv("data/all_sent_data.csv"))


def download_files():
    # https://drive.google.com/file/d/1EnRH_VD5a4HFTT8AJI745qAVtCrnYVHb/view?usp=sharing
    paras_file = "18ufw1loPZAghx0xQqlUtvTSNWt7dRmet"
    sentences_data = "1EnRH_VD5a4HFTT8AJI745qAVtCrnYVHb"


    if os.path.exists("data"):
        pass
    else:
        os.mkdir("data")

    #download the pb
    if os.path.exists("./data/all_sentence_data.csv"):
        pass
    else:
        gdd.download_file_from_google_drive(file_id=f'{paras_file}',
                                    dest_path='./data/all_sent_data.csv')

    #download the pb
    if os.path.exists("./data/sentence_data.csv"):
        pass
    else:
        gdd.download_file_from_google_drive(file_id=f'{sentences_data}',
                                    dest_path='./data/sentence_data.csv')

def search(search_terms, df, df2):
    matches = []
    sentences = df.sentences.tolist()
    # similar = df.matches.tolist()
    hits = df2.total_hits
    sent_nums = df2.sent_nums
    all_hits = []
    x=0

    for sentence in sentences:
        new = sentence.translate(str.maketrans('', '', string.punctuation))
        new_words = new.split()
        final_news = []
        for word in new_words:
            word = word.lower()
            final_news.append(word)
        found = False
        for term in search_terms:
            if term in final_news:
                if sentence not in matches:
                    matches.append(sentence)
                    found = True
        if found == True:
            if x in sent_nums:
                y=0
                for item in sent_nums:
                    if item == x:
                        print (hits[y])
                        hit = int(hits[y].replace("[", "").replace("]", "").split(",")[0])
                        if sentences[hit] not in all_hits:
                            term_hit = False
                            for term in search_terms:
                                if term in sentences[hit]:
                                    term_hit=True
                            if term_hit== False:
                                all_hits.append(sentences[hit])
                    y=y+1


                # if similar[x] != 0:
                #     hits = similar[x].replace("[", "").replace("]", "").split(",")
                #
                #     for hit in hits:
                #         hit = int(hit)
                #         if sentence[hit] not in all_hits:
                #             all_hits.append(sentence[hit])
        x=x+1
    combined = matches+all_hits
    combined = list(set(combined))
    return (matches, all_hits)

download_files()
sentence_data = cache_df()
matches = cache_paras()


st.title("USHMM Oral Testimony Sentence Embedding Search")

search_form = st.sidebar.form("Searching Form")
search_terms = search_form.text_input("Provide a list of search terms separated by commas")
search_button = search_form.form_submit_button("Search Button")






if search_button:
    words = search_terms.split(",")
    clean_searches = []
    for word in words:
        clean_searches.append(word.strip())

    matches, all_hits = search(clean_searches, sentence_data, matches)
    st.write("Here is a list of matches that contain one of your search words:")
    st.write(matches)
    st.write("Here is a list of items that matched based on similarity:")
    st.write(all_hits)
