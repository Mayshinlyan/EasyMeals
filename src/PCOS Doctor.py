from openai import OpenAI
import streamlit as st
from GenerateImage import *
from GeneratePDF import *


st.title("Curing Your PCOS")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


def main():

    # Check if initial questions have been answered
    if "initial_questions_answered" not in st.session_state:

        # Create a form to contain the initial questions and submit button
        with st.form("initial_questions_form"):
            st.write("Welcome! Please answer a few questions to get started.")
            name = st.text_input("What's your name?")
            favFood = st.text_input("What are your favorite ingredients?")
            dislikeFood = st.text_input("What ingredients do you not like?")

            # Add a submit button
            submitted = st.form_submit_button("Submit")

            # Store responses in session state only if the form is submitted
            if submitted:
                st.session_state["initial_questions_answered"] = True
                st.session_state["name"] = name
                st.session_state["favFood"] = favFood
                st.session_state["dislikeFood"] = dislikeFood

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
                        When the patient writes “Generate MEALPLAN“:

                        The patient's name is {st.session_state.get("name")} and has pcos. The patient's like {st.session_state.get("favFood")} and dislike {st.session_state.get("dislikeFood")}.

                        Point 1: You may use the patient's favorite ingredients in the recipes as long as they are pcos friendly.
                        Point 2: Never use the patient's dislike ingredients in the recipes.
                        Step 1: Create 3 days pcos friendly recipes that includes step by step instruction to make the food. The serving size would be 2.
                        Step 2: Each day must have 3 recipes. Start the recipe with BREAKFAST: for breakfast, LUNCH: for lunch and DINNER: for dinner
                        Step 3: At the end create a shopping list for the meal plan. End the shopping list with the exact word: End of the List
                        Step 4: After generating the meal plan ask the patient to type in the word “PDF“ if they want to download the PDF version of the meal plan.
                        Step 5: Once the patient typed in PDF, say the PDF is saved to local directory.
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
                            "content": f"Hello {st.session_state.get("name")}, how can I assist you today?",
                        }
                    )

                # Force rerun the app to load the session state immediately
                st.rerun()
    else:

        # Display chat history while excluding the context
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("How can I help you?"):

            # Generate PDF if the user message contains PDF
            if "PDF" in prompt:
                convert_PDF(
                    st.session_state.messages[len(st.session_state.messages) - 1].get(
                        "content"
                    )
                )

                st.success("Done!")

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


main()
