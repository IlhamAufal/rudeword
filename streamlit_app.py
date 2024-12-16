import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from translate import Translator
import re
import dill

clean_data = dill.load(open('saveFile/clean_data.sav', 'rb'))
normalize = dill.load(open('saveFile/normalize.sav', 'rb'))
stemming = dill.load(open('saveFile/stemming.sav', 'rb'))
translate_id = dill.load(open('saveFile/translate_id.sav', 'rb'))
replace_kata_kasar = dill.load(open('saveFile/replace_kata_kasar.sav', 'rb'))
execute_function = dill.load(open('saveFile/execute_function.sav', 'rb'))

# Streamlit interface
st.title("Rude Word Replacement")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('Input Paragraph')
    footage = st.text_input('')
    result=''
    if st.button('Apply'):
        footage = clean_data(footage)
        footage = normalize(footage)
        footage = stemming(footage)
        footage = translate_id(footage)
        result = replace_kata_kasar(footage)
        # result = execute(footage)
        # st.success(result)    

with col2:
     st.subheader('Result')
     st.write(result)
