import streamlit as st
import sqlite3
import hashlib
from menu import menu_with_redirect

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.user['role'] not in ["super-admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

def admin_user_management():
    st.title("User Management")

    conn = sqlite3.connect('databases/app.db')
    c = conn.cursor()
    
    c.execute("SELECT id_user, username, role FROM Users")
    users = c.fetchall()
    user_data_list = [{"ID": user[0], "Username": user[1], "Role": user[2]} for user in users]
    
    if users:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
        col1.write("ID")
        col2.write("Username")
        col3.write("Role")
        col4.write("Edit")
        col5.write("Delete")
        
        for user in user_data_list:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
            col1.write(user["ID"])
            col2.write(user["Username"])
            col3.write(user["Role"])
            with col4:
                if st.button("Edit", key=f"edit_{user['ID']}"):
                    edit_user(user["Username"])
            with col5:
                if st.button("Delete", key=f"delete_{user['ID']}"):
                    delete_user(user["Username"])
        
        if st.button("Add new user"):
            add_user()
            
    else:
        st.write("No users found.")
    
    conn.close()

@st.experimental_dialog("Add User", width="large")
def add_user():
    with st.form("add_user"):
        username = st.text_input("Username*")
        password = st.text_input("Password*", type="password")
        role = st.selectbox(
            "Select your role:",
            ["user", "admin", "super-admin"],
        )
        # role = st.text_input("Role*")

        if st.form_submit_button("Submit"):
            if username and password and role:
                conn = sqlite3.connect('databases/app.db')
                c = conn.cursor()
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                try:
                    c.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
                    conn.commit()
                    st.success("User added successfully!")
                    st.experimental_rerun()
                except sqlite3.IntegrityError:
                    st.error("Username already exists.")
                finally:
                    conn.close()
            else:
                st.error("All fields are required.")

@st.experimental_dialog("Edit User", width="large")
def edit_user(username):
    conn = sqlite3.connect('databases/app.db')
    c = conn.cursor()
    c.execute("SELECT id_user, username, role FROM Users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    with st.form("edit_user"):
        username = st.text_input("Username*", value=user[1])
        new_password = st.text_input("New Password (leave blank to keep current password)", type="password")
        role = st.selectbox(
            "Select your role:",
            ["user", "admin", "super-admin"],
        )
        # role = st.text_input("Role*", value=user[2])

        if st.form_submit_button("Update"):
            if username and role:
                conn = sqlite3.connect('databases/app.db')
                c = conn.cursor()
                
                if new_password:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    c.execute("UPDATE User SET username = ?, password = ?, role = ? WHERE id_user = ?", (username, role, hashed_password, user[0]))
                else:
                    c.execute("UPDATE User SET username = ?, role = ? WHERE id_user = ?", (username, role, user[0]))
                    
                conn.commit()
                conn.close()
                st.success("User updated successfully!")
                st.experimental_rerun()
            else:
                st.error("Username and Name are required fields.")

@st.experimental_dialog("Delete User", width="large")
def delete_user(username):
    st.warning("Are you sure you want to delete this user? This action cannot be undone.")
    if st.button("Delete"):
        conn = sqlite3.connect('databases/app.db')
        c = conn.cursor()
        c.execute("DELETE FROM User WHERE email = ?", (username,))
        conn.commit()
        conn.close()
        st.success("User deleted successfully!")
        st.experimental_rerun()


admin_user_management()