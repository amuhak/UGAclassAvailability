# Import the Python SDK
import google.generativeai as genai
import PyPDF2
from pdf2image import convert_from_path
from urllib.request import urlretrieve
import time
import smtplib


genai.configure(api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # API key from https://aistudio.google.com/

url = "https://apps.reg.uga.edu/soc/SOCfall.pdf"  # URL for the pdf

filename = "out.pdf"

print("Downloading PDF...")
urlretrieve(url, filename)
print("PDF downloaded successfully.")

file_path = "out.pdf"

print(f"Converting PDF {file_path} to string...")
pdf_file_obj = open(file_path, "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
text = []
for page_num in range(len(pdf_reader.pages)):
    page_obj = pdf_reader.pages[page_num]
    text.append(page_obj.extract_text())
pdf_file_obj.close()
print("PDF conversion to string completed.")


def custom_key(item):
    if isinstance(item, list):
        return item[0]  # Use the first element of the list for sorting
    return item  # Use the item itself if it's a string



class_list = [   # Class list
    ["CSCI 1302", "with barnes or michael"],  # you can add extra discription in natural language like so
    "ENGL 1060H",
    "CSCI 1360",
    "CSCI 2610",
    "PSYC 1030H",
]

class_list = sorted(class_list, key=custom_key)

ans = list()


model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

should_wait = False

# Query the model for each class in the class_list
for cl in class_list:
    print(f"Querying the model for class: {cl}")
    cla = cl

    if type(cl) == list:
        cla = cl[0]
        cl = cl[0] + " " + cl[1]

    data_to_send = ""

    for i in text:
        if cla in i:
            data_to_send += i
            data_to_send += "\n"


    # prompt engineering 🤓🤓🤓
    response = model.generate_content(
        [
            data_to_send,
            f"Is there a {cl} class open (have seats available and are not closed). Your reply must be concise?",
        ]
    )
    ans.append(response.text)
    print(f"Received response for class: {cl}: {ans[-1]}")
    if should_wait:
        time.sleep(60)  # Sleep for 60 seconds between queries to steer safe api limits (I have set this very high. It can be lowered)
    should_wait = True


with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
    email_address = "From email"  
    email_password = "xxxxxxxxxxxxxxxxxxx"  # Google App passwords
    print("Logging into email...")
    connection.login(email_address, email_password)
    print("Email login successful.")
    string = ""

    for i in range(len(class_list)):
        string += f"Is there a {class_list[i]} class open? \n"
        string += ans[i] + "\n"
        string += "\n"

    send_to = [  # List of people to send to (Strings)
       ,
    ]

    send_to.sort()

    for to in send_to:
        print(f"Sending email to: {to}")
        connection.sendmail(from_addr=email_address, to_addrs=to, msg=string)
        print(f"Email sent to: {to}")