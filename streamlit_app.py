import streamlit as st
import ini_asli as rd  # Pastikan ini_asli.py ada di direktori yang sama

st.title("Rude Word Replacement")

# Membuat dua kolom
col1, col2 = st.columns(2)

with col1:
    # Input teks dari pengguna
    footage = st.text_input('Input paragraph')

with col2:
    if st.button('Apply'):
        try:
            result = rd.execute(footage)
            st.success(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
