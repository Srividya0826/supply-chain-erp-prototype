import streamlit as st

st.write("Testing experimental rerun")

if st.button("Rerun app"):
    st.experimental_rerun()
