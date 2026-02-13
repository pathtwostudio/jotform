import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("JOTFORM_API_KEY")
BASE_URL = "https://api.jotform.com"

questions = {
    "questions[0][type]":     "control_head",
    "questions[0][text]":     "Incident Report Form",
    "questions[0][order]":    "1",
    "questions[0][name]":     "header",

    "questions[1][type]":     "control_textbox",
    "questions[1][text]":     "Company Name",
    "questions[1][order]":    "2",
    "questions[1][name]":     "companyName",
    "questions[1][required]": "Yes",

    "questions[2][type]":     "control_datetime",
    "questions[2][text]":     "Date of Incident",
    "questions[2][order]":    "3",
    "questions[2][name]":     "incidentDate",
    "questions[2][required]": "Yes",

    "questions[3][type]":     "control_textbox",
    "questions[3][text]":     "Incident Title",
    "questions[3][order]":    "4",
    "questions[3][name]":     "incidentTitle",
    "questions[3][required]": "Yes",

    "questions[4][type]":     "control_textarea",
    "questions[4][text]":     "Incident Description",
    "questions[4][order]":    "5",
    "questions[4][name]":     "incidentDescription",
    "questions[4][required]": "Yes",

    # Configurable List widget for dynamic Actions
    "questions[5][type]":         "control_widget",
    "questions[5][text]":         "Actions",
    "questions[5][order]":        "6",
    "questions[5][name]":         "actions",
    "questions[5][required]":     "No",
    "questions[5][widgetCode]":   "533946093c1ad0c45d000070",
    "questions[5][fields]":       "Description: text\nAssigned To: text\nDue Date: dateInput",

    "properties[title]":          "Incident Report Form",
}

response = requests.post(
    f"{BASE_URL}/user/forms",
    params={"apiKey": API_KEY},
    data=questions,
)

data = response.json()
if response.ok and data.get("responseCode") == 200:
    form_id = data["content"]["id"]
    print(f"Form created successfully!")
    print(f"Form ID:  {form_id}")
    print(f"Edit URL: https://www.jotform.com/build/{form_id}")
else:
    print(f"Error creating form: {data}")
