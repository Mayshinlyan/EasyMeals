from openai import OpenAI
import streamlit as st
from GenerateImage import *
from GeneratePDF import *
from Auth import *
from dotenv import load_dotenv
import os
from Database import *

st.set_page_config(page_title="EasyMeals", page_icon=":green_salad:" )

# Load variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

st.markdown("<h1 style='text-align: center; color: black;'>EasyMeals for PCOS</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .centered-image {
        display: block;
        width: 70%;
        margin: 5rem auto;
        border-radius: 0.5rem;
    }
    </style>

    <img src="https://images.unsplash.com/photo-1543352632-5a4b24e4d2a6?q=80&w=3425&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="centered-image">
    """,
    unsafe_allow_html=True,
)
    # If not, then initialize it
if 'connected' not in st.session_state:
    st.session_state['connected'] = False

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"
        # Check if 'key' already exists in session_state



# Authenticate the user
doAuth()


def main():

    # Check if initial questions have been answered
    if st.session_state.get("onboarded") == "no":
        displayOnboardForm()

    else:
        print("User just got onboarded")
        # Store the initial context and ask initial question
        setInitialContext()
        # Display the chat history and messages
        displayChatMessages()


def setInitialContext():
    # Set initial context
    if "context" not in st.session_state:
        st.session_state.context = [
            {
                "role": "assistant",
                "content": f"""

            Your name is Dr. Fiona Mcculloch, the author of 8 Steps to Reverse Your pcos: A Proven Program to Reset Your Hormones, Repair Your Metabolism, and Restore Your Fertility. You have treated thousands of women with pcos.
            You are now seeing your patient who has pcos. You use empathetic tone to help address your patients’ questions. You first greet your patient just like how a doctor would and then ask them what concerns do they have by listing the following options. You must list these options.
            - Explain TOPIC
            - Generate MEALPLAN
            When the patient writes “Explain TOPIC” give an explanation about TOPIC assuming that the patient has very little pcos knowledge. Use medical reasoning to explain the cause in details, symptoms and potential remedy and make recommend a simple shopping list at the end if needed to apply the remedy.
            When the patient writes “Generate MEALPLAN or m“:

            The patient's name is {st.session_state['user_info'].get('name')} and has pcos. The patient's like {st.session_state.get("favFood")} and dislike {st.session_state.get("dislikeFood")}.

            Point 1: You may use the patient's favorite ingredients in the recipes as long as they are pcos friendly.
            Point 2: Never use the patient's dislike ingredients in the recipes.
            Step 1: Create {st.session_state.get('NumOfDay')} days pcos friendly recipes that includes step by step instruction to make the food. The serving size would be 2.
            Step 2: Each day must have {st.session_state.get('breakfast')}, {st.session_state.get('lunch')}, {st.session_state.get('dinner')} and {st.session_state.get('snack')}
            Step 3: If Step 2 contains the word "snack", add the snack for each day at the end before the start of next day meals.
            Step 4: At the end create a shopping list for the meal plan. End the shopping list with the exact word: End of the List
            Step 5: After generating the meal plan ask the patient to type in the word “y“ if they want to get the meal plan emailed to them.
            Step 6: Once the patient typed in "PDF", say the PDF should arrive to the email within 10min.
            For what I ask you to do, take factor into consideration of the patient’s mental well being and really try to help the patient recover from the pcos symptoms. Reference the existing pcos researches and positive feedback from other pcos patients and your own researches that help women recover from the pcos symptoms.
            Ask me for the first task.
            CAPS LOCK words are placeholders for content inputted by the patient. Content enclosed in “double quotes” indicates what the patient types in. The patient can end the current command anytime by typing “menu” and you tell them to input any of the following:
            - Explain TOPIC
            - Generate MEALPLAN,

            """,
            },
        ]

    if "messages" not in st.session_state:
        st.session_state.messages = st.session_state.context

        # Add an initial assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Hello {st.session_state['user_info'].get('name')}, you meal preference well noted. How can I assist you today? Type 'm' if you want me to generate a mealplan for you.",
            }
        )


def displayOnboardForm():

    # Create a form to contain the initial questions and submit button
    with st.form("initial_questions_form"):
        st.write(
            f"Welcome {st.session_state["user_info"].get("name")}! Please answer a few questions to get started."
        )
        favFood = st.text_input("What are your favorite ingredients?")
        dislikeFood = st.text_input("What ingredients do you not like?")

        st.write("What types of meal do you need meal planning help with?")
        breakfast = st.checkbox("Breakfast")
        lunch = st.checkbox("Lunch")
        dinner = st.checkbox("Dinner")
        snack = st.checkbox("Snack")

        NumOfDay = st.number_input(
            "Number of Days for Meal Planning",
            min_value=1,
            max_value=14,
            value=3,
            step=1,
        )

        # Add a submit button
        submitted = st.form_submit_button("Submit")

        want_breakfast = "0"
        want_lunch = "0"
        want_dinner = "0"
        want_snack = "0"

        # Store responses in session state only if the form is submitted
        if submitted:
            if breakfast:
                want_breakfast = "1"

            if lunch:
                want_lunch = "1"

            if dinner:
                want_dinner = "1"

            if snack:
                want_snack = "1"

            insert_patients_value = (
                st.session_state["user_info"].get("name"),
                st.session_state["user_info"].get("email"),
                "1",
                favFood,
                dislikeFood,
                want_breakfast,
                want_lunch,
                want_dinner,
                want_snack,
                NumOfDay,
            )

            onboard_user(insert_patients_value)
            # Force rerun the app to load the session state immediately
            st.rerun()


def displayChatMessages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        # Add an initial assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Hello {st.session_state['user_info'].get('name')}, how can I assist you today? Type 'm' if you want me to generate a mealplan for you.",
            }
        )

    # Display chat history while excluding the context
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help you?"):

        # Generate PDF if the user message contains PDF
        if "PDF" in prompt:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Your personalized mealplan should arrive in your email within 10min.",
                }
            )
            convert_PDF(
                client,
                st.session_state.messages[len(st.session_state.messages) - 1].get(
                    "content"
                ),
                st.session_state.get("NumOfDay"),
            )

            # st.success("Done!")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})


if st.session_state["connected"]:
    main()
