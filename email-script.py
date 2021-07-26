from email.message import EmailMessage
from credential import EMAIL_ADDRESS, EMAIL_PASSWORD
from email.message import EmailMessage
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection_group("students").get()
for doc in docs:
    email01 = doc.to_dict()["email"]
    name01 = doc.to_dict()["firstName"]
    SAP = doc.to_dict()["sapID"]
    grad_year = doc.to_dict()["graduationYear"]
    course = doc.to_dict()["course"]

    msg = EmailMessage()
    msg["Subject"] = "Generated CV"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email01
    # msg["To"] = "shivanshusingh10@gmail.com"
    msg.set_content("Your CV is Here:")

    msg.add_alternative(
        """\
		<!DOCTYPE html>
		<html>
			<body>
            Hey,<br>
                Your cv is attached to this email. If you have any concerns and want to change your CV, you can do one of the following:<br>
                    1. You can delete the data from the form and then re-fill it.
                    Please send a request as a trail to this email if doing so, then we can resend your CV to you.<br>
                        Or<br>
                    2. You can fill out the Latex template attached to this email with your information.<br>
                    Mathur sir has already provided the steps for running the template. You can attach your updated CV to this email as a trail.<br>
                <br>
            Thanks and regards,<br>
            Placement committee,<br>
            STME NMIMS Navi Mumbai
			</body>
		</html>    
		""",
        subtype="html",
    )
    try:
        with open(f"pdf/{course}-{grad_year}/{SAP}.pdf", "rb") as f:
            file_data = f.read()
            file_name = f.name

        with open(f"logo.jpeg", "rb") as img01:
            img_data = img01.read()
            img_name = img01.name

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=f"{SAP}.pdf",
        )

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=f"{SAP}.tex",
        )

        msg.add_attachment(
            img_data, maintype="application", subtype="octet-stream", filename=img_name
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            try:
                smtp.send_message(msg)
            except Exception as er:
                print(er)
    except Exception as er2:
        print(er2)
