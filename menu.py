import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/upload.py", label="Uploads")
    st.sidebar.page_link("pages/real-time.py", label="Real-time Monitoring")
    if st.session_state.user['role'] in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage Blocked IPs")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.user['role'] != "super-admin",
        )
    st.sidebar.page_link("pages/logout.py", label="Log out")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("pages/login.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "logged_in" not in st.session_state or st.session_state.user is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "logged_in" not in st.session_state or st.session_state.user is None:
        st.switch_page("app.py")
    menu()