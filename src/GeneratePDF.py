from GenerateImage import *
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import streamlit as st
from SendEmail import *


# Spinner icon
def spinner():
    st.spinner("Crafting your Superb Meal Plan is. Wait for it...")


# Convert String to PDF using markdown-pdf
def convert_PDF(client, body, NumOfDay):

    # with st.spinner("Crafting your Superb Meal Plan. Wait for it..."):
    meal_list = generate_meal_image(client, body, NumOfDay)

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(
        Section(
            f"# {NumOfDay} Days PCOS Meal Plan\n\n![python](./7-Day-PCOS-Meal-Plan.png)\n"
        ),
        user_css="h1 {text-align:center;}",
    )

    for index, value in enumerate(meal_list):
        if index < NumOfDay:

            if st.session_state.get("breakfast") == "breakfast":
                pdf.add_section(
                    Section(
                        f"![python](./Day_{index+1}_breakfast.jpg)\n"
                        + grab_text_between(value, f"Day {index+1}", "Lunch:")
                    )
                )

            if st.session_state.get("lunch") == "lunch":
                pdf.add_section(
                    Section(
                        f"![python](./Day_{index+1}_lunch.jpg)\n"
                        + grab_text_between(value, "Lunch:", "Dinner:")
                    )
                )

            if st.session_state.get("dinner") == "dinner":
                pdf.add_section(
                    Section(
                        f"![python](./Day_{index+1}_dinner.jpg)\n"
                        + grab_text_after(value, "Dinner:")
                    )
                )

            if st.session_state.get("snack") == "snack":
                pdf.add_section(
                    Section(
                        f"![python](./Day_{index+1}_snack.jpg)\n"
                        + grab_text_after(value, "Snack:")
                    )
                )

        else:
            pdf.add_section(Section(value))

    pdf.meta["title"] = f"PCOS {NumOfDay} Days Meal Plan"
    pdf.meta["author"] = "PCOS Doc"
    filename = f"PCOS {NumOfDay+1} Days Meal Plan.pdf"
    pdf.save(filename)

    send_emails(
        st.session_state["user_info"].get("name"),
        st.session_state["user_info"].get("email"),
        filename,
    )

    return "done"
