import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# setup smtp server and port
smtp_port = 587
smtp_server = "smtp.gmail.com"

# login info
email_from = "hwai@u.rochester.edu"

email_pass = os.getenv("SMTP_GMAIL_PASS")

# subject of the message
subject = "Your Customized Meal Plan is ready! Please see the attached PDF. "


def send_emails(name, email_to, meal_plan_file):

    # Make the body of the email
    body = f"""
        Hi {name}
        Attached is your Customized Meal Plan!
        Thanks for using the PCOS Doctor
        Enjoy!
        """

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, "plain"))

    # Define the file to attach
    filename = meal_plan_file

    # Open the file in python as a binary
    attachment = open(filename, "rb")  # r for read and b for binary

    # Encode as base 64
    attachment_package = MIMEBase("application", "octet-stream")
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header(
        "Content-Disposition", "attachment; filename= " + filename
    )
    msg.attach(attachment_package)

    # Cast as string
    text = msg.as_string()

    try:
        print("connecting to server...")
        print(f"my secret key is {email_pass} ")
        email_server = smtplib.SMTP(smtp_server, smtp_port)
        email_server.starttls()
        email_server.login(email_from, email_pass)
        print("connected to server...")

        print(f"sending email to: {email_to}")
        email_server.sendmail(email_from, email_to, text)
        print(f"email successfully sent to: {email_to}")
    except Exception as e:
        print(e)
    finally:
        email_server.quit()

    # Run the function
