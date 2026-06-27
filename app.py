import streamlit as st

from nlp_processor import check_information
from ai_model import generate_certificate
from pdf_generator import create_certificate, convert_pdf


# Page settings
st.set_page_config(
    page_title="AI Certificate Generator",
    layout="centered"
)


# Title

st.title("🤖 AI Certificate Generator Tool")

st.write(
    "This prototype automatically creates professional certificates."
)


# ---------------- INPUT FIELDS ----------------


name = st.text_input(
    "Participant Name",
    placeholder="Enter name"
)


achievement = st.text_input(
    "Achievement / Course",
    placeholder="Example: AI Workshop Completion"
)



certificate_type = st.selectbox(

    "Certificate Type",

    [
        "Certificate of Completion",
        "Certificate of Achievement",
        "Certificate of Participation"
    ]

)



organization = st.text_input(

    "Organization Name",

    placeholder="Organization"

)



date = st.date_input(
    "Date"
)



message = st.text_area(

    "Additional Message",

    value=
    "This certificate is awarded for outstanding performance and successful completion."

)







# ---------------- GENERATE BUTTON ----------------

if st.button("Generate Certificate"):

    data = {
        "name": name,
        "event": achievement,
        "date": str(date)
    }

    missing = check_information(data)

    if missing:
        st.error("Missing information: " + str(missing))

    else:
        # 1. Your AI generates the customized text block
        ai_message = generate_certificate(
            name,
            achievement,
            message,
            str(date),
            certificate_type,
            organization
        )

        # 2. Pass the variables to create_certificate. 
        # It returns the image dimensions (w, h) so the PDF copies it exactly!
        w, h = create_certificate(
            name=name,
            course=achievement,
            cert_type=certificate_type,
            organization=organization,
            date=str(date),
            message=ai_message
        )

        # 3. Convert to PDF using the structural template dimensions
        convert_pdf(w, h)

        st.success("Certificate Generated Successfully!")

        st.image(
            "output/certificate.png",
            caption="Generated Certificate"
        )



# ---------------- DOWNLOAD BUTTON ----------------


if st.button("Print / Save PDF"):


    with open(
        "output/certificate.pdf",
        "rb"
    ) as file:


        st.download_button(

            label="Download Certificate PDF",

            data=file,

            file_name="certificate.pdf",

            mime="application/pdf"

        )