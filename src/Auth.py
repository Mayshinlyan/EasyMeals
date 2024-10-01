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

        # check if onboarded
        # if no st.session state onboarded no
        # if yes do nth and take the user to the chatbot
        # st session state onboarded yes
        email = st.session_state["user_info"].get("email")
        user_info = get_user_info(email)
        if user_info[3] == "0":
            st.session_state["onboarded"] = "no"
        else:
            st.session_state["onboarded"] = "yes"
        print(user_info)

        if st.button("Log out"):
            authenticator.logout()
