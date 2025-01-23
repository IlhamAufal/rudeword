import streamlit as st
import dill

normalize = dill.load(open('normalize.sav', 'rb'))
stemming = dill.load(open('stemming.sav', 'rb'))
translate_id = dill.load(open('translate_id.sav', 'rb'))
replace_kata_kasar = dill.load(open('replace_kata_kasar.sav', 'rb'))
tfidf_vectorizer = dill.load(open('tfidf_vectorizer.sav', 'rb'))
model_naive_bayes = dill.load(open('model_naive_bayes.sav', 'rb'))

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
            result = f"Processed: {footage}"
            sentiment_result = "positif"
            
            setattr(project_form, 'input_text', footage)
            setattr(project_form, 'sentiment_result', sentiment_result)
            setattr(project_form, 'final_text', result)

with col2:
    st.subheader('Result')
    st.write("Processed Text:")
    st.write(result)
    st.write("Sentiment:")
    st.write(sentiment_result)
