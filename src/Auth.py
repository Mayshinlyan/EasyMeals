import streamlit as st
from streamlit_google_auth import Authenticate
from Database import *


def doAuth():

    authenticator = Authenticate(
        secret_credentials_path="google_credentials.json",
        cookie_name="my_cookie_name",
        cookie_key="this_is_secret",
        redirect_uri="http://localhost:8501",
    )

    # Check if the user is already authenticated
    authenticator.check_authentification()

    # Display the login button if the user is not authenticated
    authenticator.login()

    # Display the user information and logout button if the user is authenticated
    if st.session_state["connected"]:
        # st.image(st.session_state["user_info"].get("picture"))
        # st.write(f"Hello, {st.session_state['user_info'].get('name')}")
        # st.write(f"Your email is {st.session_state['user_info'].get('email')}")

        # fetch user info and store it in the session state
        fetchUserInfo()

        if st.button("Log out"):
            authenticator.logout()


def fetchUserInfo():
    email = st.session_state["user_info"].get("email")
    user_info = get_user_info(email)
    if user_info == None:
        st.session_state["onboarded"] = "no"
    else:
        st.session_state["onboarded"] = "yes"

        # Store all user info in the session state
        st.session_state["favFood"] = user_info[4]
        st.session_state["dislikeFood"] = user_info[5]
        if user_info[6] == "1":
            st.session_state["breakfast"] = "breakfast"
        else:
            st.session_state["breakfast"] = ""

        if user_info[7] == "1":
            st.session_state["lunch"] = "lunch"
        else:
            st.session_state["lunch"] = ""

        if user_info[8] == "1":
            st.session_state["dinner"] = "dinner"
        else:
            st.session_state["dinner"] = ""

        if user_info[9] == "1":
            st.session_state["snack"] = "snack"
        else:
            st.session_state["snack"] = ""

        st.session_state["NumOfDay"] = user_info[10]

        print(user_info)
