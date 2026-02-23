#!/usr/bin/env python3
"""Create JotForm Incident Reporting Form with up to 20 incidents."""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("JOTFORM_API_KEY")
BASE_URL = "https://api.jotform.com"

def api_post(path, data):
    r = requests.post(f"{BASE_URL}{path}", params={"apiKey": API_KEY}, data=data)
    result = r.json()
    if result.get("responseCode") not in (200, 201):
        print(f"  WARNING {path}: {result.get('responseCode')} – {result.get('message')}")
    return result

def api_get(path):
    r = requests.get(f"{BASE_URL}{path}", params={"apiKey": API_KEY})
    return r.json()

MAX_INCIDENTS = 20
WIDGET_ID  = "533946093c1ad0c45d000071"
WIDGET_SRC = "https://widgets.jotform.io/configurableList/index.html"

# ── Build question flat-dict ─────────────────────────────────────────────────
q = {}
idx = 0

def qset(**props):
    global idx
    q[f"questions[{idx}][order]"] = str(idx + 1)
    for k, v in props.items():
        q[f"questions[{idx}][{k}]"] = str(v)
    idx += 1

# Main heading
qset(
    type="control_head",
    text="Incident Reporting Form",
    subHeader="Describe the details of the incident occurring.",
    name="main_header",
)

for n in range(1, MAX_INCIDENTS + 1):
    hidden = "Yes" if n > 1 else "No"

    qset(type="control_head", text=f"Incident {n}",
         name=f"incident{n}_header", hidden=hidden)

    qset(type="control_textbox", text="Incident Title",
         name=f"incident{n}_title",
         required="Yes" if n == 1 else "No",
         hidden=hidden)

    qset(type="control_textarea", text="Incident Description",
         name=f"incident{n}_description",
         required="Yes" if n == 1 else "No",
         hidden=hidden)

    qset(
        type="control_widget",
        text="Actions",
        name=f"incident{n}_actions",
        selectedField=WIDGET_ID,
        frameSrc=WIDGET_SRC,
        finalSrc=WIDGET_SRC,
        widgetType="field",
        fields="*Action Description:textarea:\n*Responsible Person:text:\n*Due Date:dateInput:",
        minRowsNumber="0",
        limit="10",
        labelAdd="+ Add Action",
        labelRemove="x",
        settingNames="fields,minRowsNumber,limit,customCSS,labelAdd,labelRemove,isTableView",
        widgetTabs='[["general","settingNames"],["customcss","settingNamesCSS"]]',
        required="No",
        hidden=hidden,
        shrink="No",
        static="No",
        newLine="No",
        theme="default",
        boxAlign="Left",
    )

    if n < MAX_INCIDENTS:
        qset(
            type="control_radio",
            text="Do you need to report another incident?",
            name=f"incident{n}_another",
            options="Yes\nNo",
            required="No",
            hidden=hidden,
        )

# Submit button
qset(type="control_button", text="Submit Incident Report", name="submit_btn")

# ── Form properties ──────────────────────────────────────────────────────────
q["properties[title]"] = "Incident Reporting Form"
q["properties[font]"] = "Inter"
q["properties[fontsize]"] = "16"
q["properties[styles]"] = "nova"
q["properties[defaultTheme]"] = "v2"
q["properties[v4]"] = "1"
q["properties[formWidth]"] = "752"
q["properties[labelWidth]"] = "230"
q["properties[highlightLine]"] = "Enabled"
q["properties[clearFieldOnHide]"] = "enable"
q["properties[injectCSS]"] = (
    ".form-all { width: 90% !important; max-width: 90% !important; }"
)
q["properties[styleJSON]"] = json.dumps({
    "@fontFamily": "Inter",
    "@fontSize": "16",
    "@labelAlign": "Top",
    "@labelWidth": "230",
    "@formWidth": "752",
    "@clrText": "#2C3345",
    "@selectedScheme": "clr-default",
    "@clrBg": "#F3F3FE",
    "@clrFrame": "#FFFFFF",
    "@clrInput": "#FFFFFF",
    "@clrActive": "#F1F5FF",
    "@clrErrorBg": "#FFF4F4",
    "@clrLabel": "#2C3345",
    "@fontLink": "//cdn.jotfor.ms/fonts/?family=Inter",
})

# ── Create form ──────────────────────────────────────────────────────────────
print(f"Creating form with {idx} questions...")
resp = api_post("/user/forms", q)
form_id = resp["content"]["id"]
print(f"Form ID : {form_id}")
print(f"URL     : https://www.jotform.com/form/{form_id}")

# ── Get question IDs ─────────────────────────────────────────────────────────
qs_resp = api_get(f"/form/{form_id}/questions")
name_to_id = {v.get("name", ""): k for k, v in qs_resp["content"].items()}

# ── Build conditional logic ──────────────────────────────────────────────────
conditions = {}
for n in range(1, MAX_INCIDENTS):
    trigger_id = name_to_id.get(f"incident{n}_another")
    if not trigger_id:
        print(f"  WARNING: no trigger for incident {n}")
        continue

    targets = [
        f"incident{n+1}_header",
        f"incident{n+1}_title",
        f"incident{n+1}_description",
        f"incident{n+1}_actions",
    ]
    if n + 1 < MAX_INCIDENTS:
        targets.append(f"incident{n+1}_another")

    ci = n - 1
    conditions[f"conditions[{ci}][id]"]                     = str(n)
    conditions[f"conditions[{ci}][enabled]"]                = "1"
    conditions[f"conditions[{ci}][type]"]                   = "field"
    conditions[f"conditions[{ci}][conditions][0][id]"]      = "1"
    conditions[f"conditions[{ci}][conditions][0][field]"]   = trigger_id
    conditions[f"conditions[{ci}][conditions][0][operator]"]= "equals"
    conditions[f"conditions[{ci}][conditions][0][value]"]   = "Yes"
    conditions[f"conditions[{ci}][logic]"]                  = "ALL"

    for ai, target_name in enumerate(targets):
        target_id = name_to_id.get(target_name)
        if target_id:
            conditions[f"conditions[{ci}][actions][{ai}][id]"]    = str(ai + 1)
            conditions[f"conditions[{ci}][actions][{ai}][action]"] = "show"
            conditions[f"conditions[{ci}][actions][{ai}][field]"]  = target_id

print(f"Setting up {MAX_INCIDENTS - 1} conditional rules...")
cond_resp = api_post(f"/form/{form_id}/conditions", conditions)
print(f"Conditions: {cond_resp.get('responseCode')} – {cond_resp.get('message')}")

print(f"\nDone! https://www.jotform.com/form/{form_id}")
