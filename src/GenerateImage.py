import urllib.request as urllib
import streamlit as st


# from diffusers import StableDiffusionPipeline
# def smaller_image():


#     # Load the Stable Diffusion model
#     pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

#     # Generate a 512x512 image
#     image = pipe("a beautiful landscape", height=512, width=512).images[0]

#     # Save or display the image
#     image.save("output.png")


# Generate Image from user prompt
def get_image_from_DALL_E_3_API(
    client,
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


# grab text after a phrase including the pharse
def grab_text_after(text, start_phrase):
    if text is not None:
        # Find the index where the start phrase occurs
        start_index = text.find(start_phrase)

        # If the start phrase is found, return the text from the start phrase onward
        if start_index != -1:
            return text[start_index:]

    return None  # Return None if the start phrase is not found


# Break down the meal plan by days and generate images
def generate_meal_image(client, body, NumOfDay):
    meal_list = []

    for i in range(1, NumOfDay):
        meal_list.append(grab_text_between(body, f"Day {i}", f"Day {i+1}"))

    meal_list.append(grab_text_between(body, f"Day {NumOfDay}", "Shopping"))
    meal_list.append(grab_text_between(body, "Shopping", "End of the List"))

    for index, value in enumerate(meal_list):
        if index != NumOfDay:

            if st.session_state.get("breakfast") == "breakfast":
                # grab breakfast prompt
                dish_prompt_breakfast = grab_text_between(
                    value, f"Day {index+1}", "Ingredients"
                )
                url_breakfast = get_image_from_DALL_E_3_API(
                    client, dish_prompt_breakfast
                )
                urllib.urlretrieve(url_breakfast, f"Day_{index+1}_breakfast.jpg")

            if st.session_state.get("lunch") == "lunch":
                dish_prompt_lunch = grab_text_between(value, f"Lunch:", "Ingredients")
                url_lunch = get_image_from_DALL_E_3_API(client, dish_prompt_lunch)
                urllib.urlretrieve(url_lunch, f"Day_{index+1}_lunch.jpg")

            if st.session_state.get("dinner") == "dinner":
                dish_prompt_dinner = grab_text_between(value, f"Dinner:", "Ingredients")
                url_dinner = get_image_from_DALL_E_3_API(client, dish_prompt_dinner)
                urllib.urlretrieve(url_dinner, f"Day_{index+1}_dinner.jpg")

            # dish_prompt_snack = grab_text_between(value, f"SNACK:", "Ingredients")
            # url_snack = get_image_from_DALL_E_3_API(client, dish_prompt_snack)
            # urllib.urlretrieve(url_snack, f"Day_{index+1}snack.jpg")

    return meal_list
