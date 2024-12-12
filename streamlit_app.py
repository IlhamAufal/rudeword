import streamlit as st
import ini_asli.ipynb as rd

st.title("Rude Word Replacement")

col1, col2 = st.columns(2)

with col1:
    footage = st.text_input('Input paragraph')

with col2:
    if st.button('Apply'):
        try:
            result = rd.execute(footage)
            st.success(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
