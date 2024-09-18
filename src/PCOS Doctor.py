from openai import OpenAI
import streamlit as st
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
from IPython.display import display, Image
import urllib.request as urllib
import re


st.title("Curing Your PCOS")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

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

        The patient's name is May and has pcos. The patient's like chicken and avocado and dislike creamy stuff.

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


# Display chat history while excluding the context
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Generate Image from user prompt
def get_image_from_DALL_E_3_API(
    user_prompt,
    image_dimension="1024x1024",
    image_quality="hd",
    model="dall-e-3",
    nb_final_image=1,
):
    response = client.images.generate(
        model=model,
        prompt=user_prompt,
        size=image_dimension,
        quality=image_quality,
        n=nb_final_image,
    )

    image_url = response.data[0].url

    return image_url


# grab text between two phrases but exclude the two phrases
def grab_text_between(text, start_phrase, end_phrase):
    if text != None:
        lines = text.splitlines()  # Split the text into individual lines
        start_index = None
        end_index = None

    # Find the index of the start phrase and end phrase
    for i, line in enumerate(lines):
        if start_phrase in line and start_index is None:
            start_index = i
        if end_phrase in line and start_index is not None:
            end_index = i
            break

    # If both start and end indices are found, return the lines between
    if start_index is not None and end_index is not None:
        return "\n".join(lines[start_index:end_index])

    return None  # Return None if no match is found


# grab text between two phrases but include the start phrase but not the end phrase
def grab_text_between_include(text, start_phrase, end_phrase):
    if text is not None:
        lines = text.splitlines()  # Split the text into individual lines
        start_index = None
        end_index = None

        # Find the index of the start phrase and end phrase
        for i, line in enumerate(lines):
            if start_phrase in line and start_index is None:
                start_index = i  # Start after finding the start phrase
            if end_phrase in line and start_index is not None:
                end_index = i  # Stop when the end phrase is found
                break

        # If both start and end indices are found, return the lines between
        if start_index is not None and end_index is not None:
            selected_lines = lines[
                start_index:end_index
            ]  # Exclude the line with end phrase
            selected_lines[0] = selected_lines[0][
                selected_lines[0].find(start_phrase) :
            ]  # Include start phrase
            return "\n".join(selected_lines)

    return None  # Return None if no match is found


# grab text after a phrase including the pharse
def grab_text_after(text, start_phrase):
    if text is not None:
        # Find the index where the start phrase occurs
        start_index = text.find(start_phrase)

        # If the start phrase is found, return the text from the start phrase onward
        if start_index != -1:
            return text[start_index:]

    return None  # Return None if the start phrase is not found


NumOfDay = 3


# Break down the meal plan by days and generate images
def generate_meal_image(body):
    # NumOfDay = st.session_state.context.get("NumOfDays")
    # print("This is the num of day:" + NumOfDay)
    meal_list = []

    for i in range(1, NumOfDay):
        meal_list.append(grab_text_between(body, f"Day {i}", f"Day {i+1}"))

    meal_list.append(grab_text_between(body, f"Day {NumOfDay}", "Shopping"))
    meal_list.append(grab_text_between(body, "Shopping", "End of the List"))

    for index, value in enumerate(meal_list):
        if index != NumOfDay:
            # grab breakfast prompt
            dish_prompt_breakfast = grab_text_between(
                value, f"Day {index+1}", "Ingredients"
            )
            print(dish_prompt_breakfast)
            url_breakfast = get_image_from_DALL_E_3_API(dish_prompt_breakfast)
            urllib.urlretrieve(url_breakfast, f"Day_{index+1}_breakfast.jpg")

            dish_prompt_lunch = grab_text_between(value, f"LUNCH:", "Ingredients")
            url_lunch = get_image_from_DALL_E_3_API(dish_prompt_lunch)
            urllib.urlretrieve(url_lunch, f"Day_{index+1}_lunch.jpg")

            dish_prompt_dinner = grab_text_between(value, f"DINNER:", "Ingredients")
            url_dinner = get_image_from_DALL_E_3_API(dish_prompt_dinner)
            urllib.urlretrieve(url_dinner, f"Day_{index+1}_dinner.jpg")

    return meal_list
    # meal_list.append(grab_text_between(body, "Day 7", "Day 2"))


# Spinner icon
def spinner():
    st.spinner("Crafting your Superb Meal Plan is. Wait for it...")


# Convert String to PDF using markdown-pdf
def convert_PDF(body):

    with st.spinner("Crafting your Superb Meal Plan. Wait for it..."):
        meal_list = generate_meal_image(body)

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(
        Section("# 7 Days PCOS Meal Plan\n\n![python](./7-Day-PCOS-Meal-Plan.png)\n"),
        user_css="h1 {text-align:center;}",
    )

    for index, value in enumerate(meal_list):
        if index < NumOfDay:

            pdf.add_section(Section(f"![python](./Day_{index+1}_breakfast.jpg)\n"))
            pdf.add_section(
                Section(grab_text_between_include(value, f"Day {index+1}", "LUNCH:"))
            )

            pdf.add_section(Section(f"![python](./Day_{index+1}_lunch.jpg)\n"))
            pdf.add_section(
                Section(grab_text_between_include(value, "LUNCH:", "DINNER:"))
            )

            pdf.add_section(Section(f"![python](./Day_{index+1}_dinner.jpg)\n"))
            pdf.add_section(Section(grab_text_after(value, "DINNER:")))

        else:
            pdf.add_section(Section(value))

    pdf.meta["title"] = "PCOS 7 Days Meal Plan"
    pdf.meta["author"] = "PCOS Doc"
    pdf.save("PCOS 7 Days Meal Plan.pdf")

    return "done"


def main():

    # Accept user input
    if prompt := st.chat_input("Welcome! How can I help you?"):

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
