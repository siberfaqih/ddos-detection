import streamlit as st
import sqlite3
import hashlib

def create_connection():
    return sqlite3.connect('databases/app.db')

def register_user():
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin", "super-admin"])

    if st.button("Register"):
        try:
            conn = create_connection()
            c = conn.cursor()

if __name__ == "__main__":
    register_user()