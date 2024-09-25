from GenerateImage import *
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import streamlit as st


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

            pdf.add_section(
                Section(
                    f"![python](./Day_{index+1}_breakfast.jpg)\n"
                    + grab_text_between(value, f"Day {index+1}", "LUNCH:")
                )
            )

            pdf.add_section(
                Section(
                    f"![python](./Day_{index+1}_lunch.jpg)\n"
                    + grab_text_between(value, "LUNCH:", "DINNER:")
                )
            )

            pdf.add_section(
                Section(
                    f"![python](./Day_{index+1}_dinner.jpg)\n"
                    + grab_text_after(value, "DINNER:")
                )
            )

        else:
            pdf.add_section(Section(value))

    pdf.meta["title"] = f"PCOS {NumOfDay} Days Meal Plan"
    pdf.meta["author"] = "PCOS Doc"
    pdf.save(f"PCOS {NumOfDay} Days Meal Plan.pdf")

    return "done"
