import streamlit as st

if st.session_state.logged_in:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.switch_page("pages/login.py")