import streamlit as st
import dill
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from translate import Translator

clean_data = dill.load(open('saveFile/clean_data.sav', 'rb'))
normalize = dill.load(open('saveFile/normalize.sav', 'rb'))
stemming = dill.load(open('saveFile/stemming.sav', 'rb'))
translate_id = dill.load(open('saveFile/translate_id.sav', 'rb'))
replace_kata_kasar = dill.load(open('saveFile/replace_kata_kasar.sav', 'rb'))
tfidf_vectorizer = dill.load(open('saveFile/tfidf_vectorizer.sav', 'rb'))
model_naive_bayes = dill.load(open('saveFile/model_naive_bayes.sav', 'rb'))

def prediksi_sentimen(text):
    teksBaru = tfidf_vectorizer.transform([text])
    prediksi = model_naive_bayes.predict(teksBaru)
    sentiment = "positif" if prediksi[0] == 1 else "netral" if prediksi[0] == 0 else "negatif"
    return sentiment

st.title("Rude Word Replacement")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('Input Words')
    footage = st.text_input('')
    result = ''
    sentiment_result = ''
    
    if st.button('Apply'):
        if footage:
            cleaned_text = clean_data(footage)
            normalized_text = normalize(cleaned_text)
            stemmed_text = stemming(normalized_text)
            translated_text = translate_id(stemmed_text)
            sentiment_result = prediksi_sentimen(translated_text)
            
            if sentiment_result != "positif":
                final_text = replace_kata_kasar(stemmed_text)
            else:
                final_text = stemmed_text
                                    
            result = final_text 
        else:
            result = "Please input words first!"
            sentiment_result = ""

with col2:
    st.subheader('Result')
    st.write("Processed Text:")
    st.write(result)
    st.write("Sentiment:")
    st.write(sentiment_result)
