import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from translate import Translator
import re
import dill

clean_data = dill.load(open('clean_data.sav', 'rb'))
normalize = dill.load(open('normalize.sav', 'rb'))
stemming = dill.load(open('stemming.sav', 'rb'))
translate_id = dill.load(open('translate_id.sav', 'rb'))
replace_kata_kasar = dill.load(open('replace_kata_kasar.sav', 'rb'))
execute_function = dill.load(open('execute_function.sav', 'rb'))

# Streamlit interface
st.title("Rude Word Replacement")

col1, col2 = st.columns(2)

with col1:
    footage = st.text_input('Input paragraph')

with col2:
    if st.button('Apply'):
            footage = clean_data(footage)
            footage = normalize(footage)
            footage = stemming(footage)
            footage = translate_id(footage)
            result = replace_kata_kasar(footage)
            # result = execute(footage)
            st.success(result)
