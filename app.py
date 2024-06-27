import streamlit as st
from menu import menu
from pages.login import login

if __name__ == "__main__":
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()

    else:
        menu()
    