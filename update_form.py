import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("JOTFORM_API_KEY")
BASE_URL = "https://api.jotform.com"
FORM_ID = "260430768025858"

# ── 1. Fix the Actions widget ────────────────────────────────────────────────
widget_update = {
    "type":        "control_widget",
    "text":        "Actions",
    "order":       "6",
    "name":        "actions",
    "required":    "No",
    "widgetCode":  "533946093c1ad0c45d000070",
    "fields":      "Description: text\nAssigned To: text\nDue Date: dateInput",
    "minRows":     "1",
    "maxRows":     "10",
    "addButton":   "Add Row",
    "deleteButton": "1",
}

r = requests.post(
    f"{BASE_URL}/form/{FORM_ID}/question/6",
    params={"apiKey": API_KEY},
    data=widget_update,
)
resp = r.json()
if resp.get("responseCode") == 200:
    print("✓ Widget question updated")
else:
    print(f"✗ Widget update failed: {resp}")

# ── 2. Apply modern CSS ───────────────────────────────────────────────────────
modern_css = """
/* === Modern Incident Report Form === */

/* Page background */
.supernova {
  background: #f0f2f5 !important;
  min-height: 100vh !important;
}

/* Form card */
.form-all {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'Helvetica Neue', Arial, sans-serif !important;
  background: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 8px 32px rgba(0,0,0,0.08) !important;
  padding: 48px 48px 40px !important;
  max-width: 680px !important;
  margin: 0 auto !important;
}

/* Header */
.form-header-group {
  border-bottom: 2px solid #f0f2f5 !important;
  padding-bottom: 28px !important;
  margin-bottom: 8px !important;
}
.form-header-group .form-header {
  font-size: 26px !important;
  font-weight: 700 !important;
  color: #111827 !important;
  letter-spacing: -0.4px !important;
}
.form-header-group .form-subHeader {
  color: #6b7280 !important;
  font-size: 14px !important;
}

/* Form lines spacing */
.form-line {
  margin-top: 0 !important;
  margin-bottom: 20px !important;
  padding-top: 4px !important;
}

/* Labels */
.form-label,
.form-label-top {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #374151 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.4px !important;
  margin-bottom: 6px !important;
}

.form-required {
  color: #ef4444 !important;
}

/* Inputs, textareas, dropdowns */
.form-textbox,
.form-textarea,
.form-dropdown,
input[type="text"],
input[type="email"],
input[type="number"],
textarea,
select {
  border: 1.5px solid #e5e7eb !important;
  border-radius: 8px !important;
  padding: 10px 14px !important;
  font-size: 15px !important;
  font-family: inherit !important;
  color: #111827 !important;
  background: #fafafa !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
  width: 100% !important;
  box-sizing: border-box !important;
}
.form-textbox:focus,
.form-textarea:focus,
input[type="text"]:focus,
textarea:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
  outline: none !important;
  background: #ffffff !important;
}

/* Datetime sub-inputs */
.form-datetime input {
  border: 1.5px solid #e5e7eb !important;
  border-radius: 8px !important;
  padding: 10px 12px !important;
  font-size: 15px !important;
  background: #fafafa !important;
}

/* Sub-labels (Day / Month / Year hints) */
.form-sub-label {
  font-size: 11px !important;
  color: #9ca3af !important;
  margin-top: 3px !important;
}

/* Submit button */
input[type="submit"],
.form-submit-button,
button[type="submit"] {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 14px 32px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  font-family: inherit !important;
  cursor: pointer !important;
  width: 100% !important;
  letter-spacing: 0.2px !important;
  transition: opacity 0.15s ease, transform 0.1s ease !important;
  margin-top: 8px !important;
}
input[type="submit"]:hover,
.form-submit-button:hover {
  opacity: 0.92 !important;
  transform: translateY(-1px) !important;
}

/* Widget iframe container */
.form-line-column iframe,
.form-line iframe {
  border-radius: 8px !important;
  border: 1.5px solid #e5e7eb !important;
}
"""

props_update = {
    "properties[injectCSS]":  modern_css,
    "properties[background]": "#f0f2f5",
    "properties[formWidth]":  "680",
    "properties[styleJSON]":  '{"@clrText":"#111827","@labelAlign":"Top","@formWidth":"680",'
                              '"@labelWidth":"150","@lineSpacing":"20","@clrFrame":"#ffffff",'
                              '"@clrLabel":"#374151"}',
}

r2 = requests.post(
    f"{BASE_URL}/form/{FORM_ID}/properties",
    params={"apiKey": API_KEY},
    data=props_update,
)
resp2 = r2.json()
if resp2.get("responseCode") == 200:
    print("✓ Form properties updated (modern CSS applied)")
else:
    print(f"✗ Properties update failed: {resp2}")

print(f"\nView form: https://www.jotform.com/{FORM_ID}")
print(f"Edit form: https://www.jotform.com/build/{FORM_ID}")
