import streamlit as st
st.title("Bonjour, Streamlit !")
st.write("Ceci est une application Streamlit minimale.")

x = st.slider('Sélectionnez une valeur')
st.write(x, 'carré est', x*x)