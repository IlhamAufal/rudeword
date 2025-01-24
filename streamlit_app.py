import streamlit as st
import Sastrawi
import json
import dill

# normalize = dill.load(open('saveFile/normalize.sav', 'rb'))
# stemming = dill.load(open('saveFile/stemming.sav', 'rb'))
# translate_id = dill.load(open('saveFile/translate_id.sav', 'rb'))
# replace_kata_kasar = dill.load(open('saveFile/replace_kata_kasar.sav', 'rb'))
tfidf_vectorizer = dill.load(open('saveFile/tfidf_vectorizer.sav', 'rb'))
model_naive_bayes = dill.load(open('saveFile/model_naive_bayes.sav', 'rb'))

def clean_data(text):
    import re
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_normalization_dict():
    with open('normalization_dict.json', 'r') as file:
        normalization_dict = json.load(file)
    return normalization_dict

def normalize(text):
    import re, json
    def load_normalization_dict():
        with open('normalization_dict.json', 'r') as file:
            normalization_dict = json.load(file)
        return normalization_dict
    normalization_dict = load_normalization_dict()
    for word, replacement in normalization_dict.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        text = re.sub(pattern, replacement, text)
    return text

def stemming(text_cleaning):
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(text_cleaning)

def translate_id(text):
    from googletrans import Translator
    try:
        translator = Translator(from_lang='en', to_lang="id" )
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Error in translation: {e}")
        return text

def replace_kata_kasar(text):
    import json
    with open('kamus_kasar.json', 'r') as file:
        kamus = json.load(file)
    kata_kasar = set(kamus.keys())
    words = text.split()
    word_replacement = [kamus[key] if key in kata_kasar else key for key in words]
    return ' '.join(word_replacement)

def prediksi_sentimen(text):
    teksBaru = tfidf_vectorizer.transform([text])
    prediksi = model_naive_bayes.predict(teksBaru)
    sentiment = "positif" if prediksi[0] == 1 else "netral" if prediksi[0] == 0 else "negatif"
    return sentiment

class ProjectForm:
    def __init__(self):
        self.input_text = ""
        self.sentiment_result = ""
        self.final_text = ""

project_form = ProjectForm()

st.title("Rude Word Replacement")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('Input Words')
    footage = st.text_input('', value=project_form.input_text)
    sentiment_result = project_form.sentiment_result
    result = project_form.final_text
    
    if st.button('Apply'):
        if footage:
            normalized_text = normalize(footage)
            stemmed_text = stemming(normalized_text)
            translated_text = translate_id(stemmed_text)
            sentiment_result = prediksi_sentimen(translated_text)
            
            if sentiment_result != "positif":
                final_text = replace_kata_kasar(stemmed_text)
            else:
                final_text = stemmed_text
            
            setattr(project_form, 'input_text', footage)
            setattr(project_form, 'sentiment_result', sentiment_result)
            setattr(project_form, 'final_text', final_text)
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
