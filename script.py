import fire
import subprocess
import os
import shutil
import json
from email.message import EmailMessage
from credential import EMAIL_ADDRESS, EMAIL_PASSWORD
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = firestore.client()


def strFormatter(text: str) -> str:
    """Return a string by parsing and escaping latex reserved chars"""

    text = str(text)

    for x in range(len(text)):
        if x == 0 and text[x] == "&":
            text = "\\" + text
        elif text[x] == "&" and text[x - 1] != "\\":
            text = text[:x] + "\\" + text[x:]

        elif x == 0 and text[x] == "%":
            text = "\\" + text
        elif text[x] == "%" and text[x - 1] != "\\":
            text = text[:x] + "\\" + text[x:]
        elif text[-1] == "%" and text[-2] != "\\":
            text = text[:-1] + "\\" + text[-1]

        elif x == 0 and text[x] == "#":
            text = "\\" + text
        elif text[x] == "#" and text[x - 1] != "\\":
            text = text[:x] + "\\" + text[x:]

        elif x == 0 and text[x] == "_":
            text = "\\" + text
        elif text[x] == "_" and text[x - 1] != "\\":
            text = text[:x] + "\\" + text[x:]
    text = text.replace('"', "``", 1)
    text = text.replace("'", "`", 1)
    text = text.replace("’", "'")
    text = text.replace("“", "``")
    text = text.replace("”", '"')
    text = text.replace("–", "-")
    text = text.replace("‘", "`")
    text = text.replace("’", "'")
    text = text.replace("•", "")
    return text


def make_pdf(s_dict: dict) -> None:
    """Single PDF generation"""

    # Read all the templates in memory
    main_template = r""""""  # Append all sub_templates to this at last stage
    internship_template = r""""""  # Append concatenated interships to this template
    project_template = r""""""  # Append concatenated projects to this template
    leadership_template = r""""""  # Append concatenated leaderships to this template
    extracurricular_template = (
        r""""""  # Append hobbies and courses and certification here
    )
    github_template = r""""""  # Append github url to this

    internship_parent = r""""""
    project_parent = r""""""
    leadership_parent = r""""""

    ending = r""""""

    with open("templates/ending.tex", "r") as fe:
        ending = fe.read()

    # Set filename
    filename = s_dict["sapID"]

    # Interpolate data into internship_template
    if len(s_dict["internship"]) > 0:

        with open("templates/internship_parent.tex") as fip:
            internship_parent = fip.read()

        for internship in s_dict["internship"]:

            with open("templates/internship_template.tex", "r") as f:

                intern_temp = r""""""
                intern_temp = f.read()

                description_main = r""""""

                for description in internship["internDesc"]:

                    with open("templates/item_template.tex", "r") as p:

                        temp = r""""""
                        temp = p.read()

                        description_main += temp % (strFormatter(description))

                internship_template += intern_temp % (
                    strFormatter(internship["orgName"]),
                    strFormatter(internship["internDur"]),
                    strFormatter(internship["internRole"]),
                    description_main,
                )

        internship_parent = internship_parent % internship_template

    # Interpolate data into project_template
    if len(s_dict["project"]) > 0:

        with open("templates/project_parent.tex") as fpp:
            project_parent = fpp.read()

        for count, project in enumerate(s_dict["project"]):

            with open("templates/project_template.tex", "r") as f:

                proj_temp = r""""""
                proj_temp = f.read()

                description_main = r""""""

                for description in project["projDesc"]:

                    with open("templates/item_template.tex", "r") as p:

                        temp = r""""""
                        temp = p.read()

                        description_main += temp % (strFormatter(description))

                project_template += proj_temp % (
                    strFormatter(project["projName"]),
                    strFormatter(project["projDur"]),
                    strFormatter(project["projTool"]),
                    description_main,
                )

        project_parent = project_parent % project_template

    # Interpolate data into leadership_template
    if len(s_dict["leadership"]) > 0:

        with open("templates/leadership_parent.tex") as flp:
            leadership_parent = flp.read()

        for leadership in s_dict["leadership"]:

            with open("templates/leadership_template.tex", "r") as f:

                lead_temp = r""""""
                lead_temp = f.read()

                description_main = r""""""

                for description in leadership["leadDesc"]:

                    with open("templates/item_template.tex", "r") as p:

                        temp = r""""""
                        temp = p.read()

                        description_main += temp % (strFormatter(description))

                leadership_template += lead_temp % (
                    strFormatter(leadership["leadName"]),
                    strFormatter(leadership["leadDur"]),
                    strFormatter(leadership["leadRole"]),
                    description_main,
                )

        leadership_parent = leadership_parent % leadership_template

    # Interpolate data into extracurricular template
    with open("templates/extracurricular.tex") as ext:
        extracurricular_template = ext.read()
        extracurricular_template = extracurricular_template % (
            strFormatter(s_dict["hobbies"]),
            strFormatter(s_dict["certificationAndCourse"]),
        )

    with open("templates/github_template.tex") as gt:
        github_template = gt.read()
        github_template = github_template % (strFormatter(s_dict["githubUrl"]))

    # Read main template from tex file
    with open("templates/resume_template.tex", "r") as f:
        main_template = f.read()

    # Interpolate data into main_template
    dat = main_template % (
        strFormatter(f"{s_dict['firstName']} {s_dict['lastName']}"),
        s_dict["mobile"],
        s_dict["mobile"],
        strFormatter(s_dict["linkedinUrl"]),
        github_template if len(s_dict["githubUrl"]) > 0 else "",
        s_dict["email"],
        s_dict["email"],
        f"{s_dict['admissionYear']}-{s_dict['graduationYear']}",
        "Btech (Computer Science and Business Systems)"
        if s_dict["course"] == "BTech"
        else "Btech (Computer Science), MBA",
        s_dict["cgpa"],
        strFormatter(s_dict["programmingLanguage"]),
        strFormatter(s_dict["toolsAndTechnologies"]),
        strFormatter(s_dict["coreSkills"]),
    )

    if len(s_dict["internship"]) > 0:
        dat += internship_parent

    if len(s_dict["project"]) > 0:
        dat += project_parent

    dat += extracurricular_template

    if len(s_dict["leadership"]) > 0:
        dat += leadership_parent

    dat += ending

    # Write new template file
    with open(f"{filename}.tex", "w") as f:
        f.write(dat)

    # Calling CLI utility
    proc = subprocess.Popen(["pdflatex", f"{filename}.tex"])
    proc.communicate()

    # Redundant file removal, may need logs for debugging
    os.unlink(f"{filename}.aux")
    os.unlink(f"{filename}.log")
    os.unlink(f"{filename}.out")

    cleanUp(s_dict["sapID"], s_dict["course"], s_dict["graduationYear"])


def cleanUp(sap, batch, gradYear):
    """Remove residual files post PDF generation"""

    batchDir = f"{batch}-{gradYear}"

    if not (os.path.exists("pdf")):
        os.mkdir("pdf")

    if not (os.path.exists(os.path.join("pdf", batchDir))):
        os.mkdir(os.path.join("pdf", batchDir))

    files = [
        f
        for f in os.listdir(".")
        if os.path.isfile(f) and (f.endswith(".pdf") or f.endswith(".tex"))
    ]

    for stuFile in files:
        shutil.move(stuFile, os.path.join("pdf", batchDir))


def createAll() -> None:
    """Generate PDF for all documents"""

    docs = db.collection_group("students").get()

    for doc in docs:
        py_dict = doc.to_dict()
        make_pdf(py_dict)


def createBatch(batch: str = "None"):
    """Generate PDF for all students in a batch"""

    docs = db.collection("student").document(f"{batch}").collection("students").get()

    for doc in docs:
        py_dict = doc.to_dict()
        make_pdf(py_dict)


def createOne(sapid: str = "0000") -> None:
    """Generate PDF for a single student"""

    docs = db.collection_group("students").where("sapID", "==", str(sapid)).stream()

    for doc in docs:
        py_dict = doc.to_dict()
        make_pdf(py_dict)


def main() -> None:
    fire.Fire()

    cred = credentials.Certificate("keys.json")
    firebase_admin.initialize_app(cred)

    # Sending Email
    docs = db.collection_group("students").get()

    for doc in docs:
        email01 = doc.to_dict()["email"]
        name01 = doc.to_dict()["firstName"]

        msg = EmailMessage()
        msg["Subject"] = "CV"
        msg["From"] = EMAIL_ADDRESS
        # msg['To'] = email01
        msg["To"] = "ritish20mohapatra@gmail.com"
        msg.set_content("Your CV is Here:")

        msg.add_alternative(
            """\
            <!DOCTYPE html>
            <html>
                <body>
                    <h3 >Here's your generated CV.
                Regards, 
                Placement committee, STME NMIMS Navi Mumba</h3>
                </body>
            </html>    
            """,
            subtype="html",
        )

        with open(f"pdf/{name01}.pdf", "rb") as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name,
        )

        # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #     smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        #     smtp.send_message(msg)


if __name__ == "__main__":
    main()
