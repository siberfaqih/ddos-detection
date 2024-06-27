import streamlit as st
import sqlite3
import hashlib

def create_connection():
    return sqlite3.connect('databases/app.db')

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            conn = create_connection()
            c = conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            c.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, hashed_password))
            user = c.fetchone()

            if user:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user = {
                        'id_user': user[0],
                        'username': user[1],
                        'role': user[3]
                }
                st.rerun()

            else:
                st.error("Invalid username or password")

            conn.close()
        except Exception as e:
            st.error(f"An error occurred while logging in: {e}")
    

if __name__ == "__main__":
   login()