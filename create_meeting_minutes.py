import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("JOTFORM_API_KEY")
BASE_URL = "https://api.jotform.com"

WIDGET_SELECTED_FIELD = "533946093c1ad0c45d000071"
WIDGET_FRAME_SRC = "https://widgets.jotform.io/configurableList/index.html"
WIDGET_TABS = json.dumps([["general", "settingNames"], ["customcss", "settingNamesCSS"]])
WIDGET_SETTING_NAMES = "fields,minRowsNumber,limit,customCSS,labelAdd,labelRemove,isTableView"

style_json = json.dumps({
    "@fontFamily":     "Inter",
    "@fontSize":       "16",
    "@labelAlign":     "Top",
    "@labelWidth":     "230",
    "@formWidth":      "752",
    "@clrText":        "#2C3345",
    "@selectedScheme": "clr-default",
    "@clrBg":          "#F3F3FE",
    "@clrFrame":       "#FFFFFF",
    "@clrInput":       "#FFFFFF",
    "@clrActive":      "#F1F5FF",
    "@clrErrorBg":     "#FFF4F4",
    "@clrLabel":       "#2C3345",
    "@fontLink":       "//cdn.jotfor.ms/fonts/?family=Inter",
})

data = {
    # ── Header ──────────────────────────────────────────────────────────────────
    "questions[0][type]":     "control_head",
    "questions[0][text]":     "Meeting Minutes",
    "questions[0][subHeader]":"Record the details, attendees, and action items from your meeting.",
    "questions[0][order]":    "1",
    "questions[0][name]":     "header",

    # ── Date of Meeting ──────────────────────────────────────────────────────────
    "questions[1][type]":     "control_datetime",
    "questions[1][text]":     "Date of Meeting",
    "questions[1][order]":    "2",
    "questions[1][name]":     "meetingDate",
    "questions[1][required]": "Yes",
    "questions[1][liteMode]": "Yes",
    "questions[1][format]":   "mmddyyyy",

    # ── Meeting Title ────────────────────────────────────────────────────────────
    "questions[2][type]":     "control_textbox",
    "questions[2][text]":     "Meeting Title",
    "questions[2][order]":    "3",
    "questions[2][name]":     "meetingTitle",
    "questions[2][required]": "Yes",

    # ── Attendees (Configurable List) ────────────────────────────────────────────
    "questions[3][type]":            "control_widget",
    "questions[3][text]":            "Attendees",
    "questions[3][order]":           "4",
    "questions[3][name]":            "attendees",
    "questions[3][required]":        "No",
    "questions[3][selectedField]":   WIDGET_SELECTED_FIELD,
    "questions[3][frameSrc]":        WIDGET_FRAME_SRC,
    "questions[3][finalSrc]":        WIDGET_FRAME_SRC,
    "questions[3][widgetType]":      "field",
    "questions[3][fields]":          "*Name:text:",
    "questions[3][minRowsNumber]":   "1",
    "questions[3][limit]":           "0",        # 0 = unlimited
    "questions[3][labelAdd]":        "+ Add Attendee",
    "questions[3][labelRemove]":     "x",
    "questions[3][isTableView]":     "undefined",
    "questions[3][label]":           "Yes",
    "questions[3][frameWidth]":      "580",
    "questions[3][frameHeight]":     "50",
    "questions[3][maxWidth]":        "587",
    "questions[3][settingNames]":    WIDGET_SETTING_NAMES,
    "questions[3][widgetTabs]":      WIDGET_TABS,
    "questions[3][shrink]":          "No",
    "questions[3][static]":          "No",
    "questions[3][newLine]":         "No",
    "questions[3][hidden]":          "No",
    "questions[3][theme]":           "default",
    "questions[3][boxAlign]":        "Left",

    # ── Meeting Overview ─────────────────────────────────────────────────────────
    "questions[4][type]":     "control_textarea",
    "questions[4][text]":     "Meeting Overview",
    "questions[4][order]":    "5",
    "questions[4][name]":     "meetingOverview",
    "questions[4][required]": "Yes",

    # ── Actions (Configurable List, max 10) ──────────────────────────────────────
    "questions[5][type]":            "control_widget",
    "questions[5][text]":            "Actions",
    "questions[5][order]":           "6",
    "questions[5][name]":            "actions",
    "questions[5][required]":        "No",
    "questions[5][selectedField]":   WIDGET_SELECTED_FIELD,
    "questions[5][frameSrc]":        WIDGET_FRAME_SRC,
    "questions[5][finalSrc]":        WIDGET_FRAME_SRC,
    "questions[5][widgetType]":      "field",
    "questions[5][fields]":          "*Action Description:textarea:\n*Due Date:dateInput:",
    "questions[5][minRowsNumber]":   "1",
    "questions[5][limit]":           "10",
    "questions[5][labelAdd]":        "+ Add Action",
    "questions[5][labelRemove]":     "x",
    "questions[5][isTableView]":     "undefined",
    "questions[5][label]":           "Yes",
    "questions[5][frameWidth]":      "580",
    "questions[5][frameHeight]":     "50",
    "questions[5][maxWidth]":        "587",
    "questions[5][settingNames]":    WIDGET_SETTING_NAMES,
    "questions[5][widgetTabs]":      WIDGET_TABS,
    "questions[5][shrink]":          "No",
    "questions[5][static]":          "No",
    "questions[5][newLine]":         "No",
    "questions[5][hidden]":          "No",
    "questions[5][theme]":           "default",
    "questions[5][boxAlign]":        "Left",

    # ── Submit Button ────────────────────────────────────────────────────────────
    "questions[6][type]":     "control_button",
    "questions[6][text]":     "Submit Meeting Minutes",
    "questions[6][order]":    "7",
    "questions[6][name]":     "submit",

    # ── Form Properties ──────────────────────────────────────────────────────────
    "properties[title]":            "Meeting Minutes",
    "properties[font]":             "Inter",
    "properties[fontsize]":         "16",
    "properties[fontcolor]":        "#2C3345",
    "properties[background]":       "#FFFFFF",
    "properties[formWidth]":        "752",
    "properties[labelWidth]":       "230",
    "properties[styles]":           "nova",
    "properties[defaultTheme]":     "v2",
    "properties[v4]":               "1",
    "properties[highlightLine]":    "Enabled",
    "properties[hideMailEmptyFields]":        "enable",
    "properties[hideEmptySubmissionFields]":  "Yes",
    "properties[errorNavigation]":            "Yes",
    "properties[styleJSON]":        style_json,
}

response = requests.post(
    f"{BASE_URL}/user/forms",
    params={"apiKey": API_KEY},
    data=data,
)

resp = response.json()
if response.ok and resp.get("responseCode") == 200:
    form_id = resp["content"]["id"]
    print("Form created successfully!")
    print(f"Form ID:  {form_id}")
    print(f"Edit URL: https://www.jotform.com/build/{form_id}")
    print(f"View URL: https://form.jotform.com/{form_id}")
else:
    print(f"Error creating form: {resp}")
