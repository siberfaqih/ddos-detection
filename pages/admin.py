import streamlit as st
import sqlite3
from menu import menu_with_redirect

menu_with_redirect()
def admin_user_management():
    st.title("Blocked IP Management")

    conn = sqlite3.connect('databases/app.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM BlockedIPs")
    ips = c.fetchall()
    ip_data_list = [{"ID": ips[0], "IP Address": ips[1], "Timestamp": ips[2]} for ip in ips]
    
    if ips:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        col1.write("ID")
        col2.write("IP Address")
        col3.write("Timestamp")
        col4.write("Delete")
        
        for ip in ip_data_list:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            col1.write(ip["ID"])
            col2.write(ip["IP Address"])
            col3.write(ip["Timestamp"])
           
            with col4:
                if st.button("Delete", key=f"delete_{ip['ID']}"):
                    delete_user(ip["Username"])
            
    else:
        st.write("No blocked IPs found.")
    
    conn.close()

@st.experimental_dialog("Delete User", width="large")
def delete_user(username):
    st.warning("Are you sure you want to delete this user? This action cannot be undone.")
    if st.button("Delete"):
        conn = sqlite3.connect('sentiment.db')
        c = conn.cursor()
        c.execute("DELETE FROM User WHERE email = ?", (username,))
        conn.commit()
        conn.close()
        st.success("User deleted successfully!")
        st.experimental_rerun()


admin_user_management()