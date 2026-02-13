# JotForm API Notes

## Authentication
- API key passed as query param: `?apiKey=...`
- Stored in `.env` as `JOTFORM_API_KEY`

## Running Scripts
- `pip`/`pip3` are not available globally on this machine
- Use `~/.local/bin/uv run --with requests --with python-dotenv python3 script.py`
- `pipx` (`/usr/bin/pipx`) is for CLI tools only, not library deps

---

## API Endpoints — Correct Methods

| Action | Method | Endpoint |
|--------|--------|----------|
| Create form | `POST` | `/user/forms` |
| Get questions | `GET` | `/form/{id}/questions` |
| Get single question | `GET` | `/form/{id}/question/{qid}` |
| Add question | `POST` | `/form/{id}/questions` — keys: `question[type]`, `question[text]`, etc. |
| Update question | `POST` | `/form/{id}/question/{qid}` — **POST not PUT** |
| Delete question | `DELETE` | `/form/{id}/question/{qid}` |
| Update properties | `POST` | `/form/{id}/properties` — keys must use `properties[key]` wrapper |
| List user forms | `GET` | `/user/forms` |

**Note:** You **cannot change a question's `type`** in-place — delete and re-add instead.

---

## Creating a Form — Flat Key Format

```python
data = {
    "questions[0][type]":     "control_textbox",
    "questions[0][text]":     "Company Name",
    "questions[0][order]":    "1",
    "questions[0][name]":     "companyName",
    "questions[0][required]": "Yes",
    "properties[title]":      "My Form",
}
requests.post(f"{BASE_URL}/user/forms", params={"apiKey": API_KEY}, data=data)
```

---

## Field Types

| Type | Notes |
|------|-------|
| `control_head` | Header/section divider. Use `text` for title, `subHeader` for subtitle. |
| `control_textbox` | Single-line text. Use `size` for width (e.g. `"310"`). |
| `control_textarea` | Multi-line text. |
| `control_datetime` | Date picker. Use `liteMode: "Yes"` for a single combined date input. `format: "mmddyyyy"`. |
| `control_button` | Submit button. Use `text` for button label. |
| `control_matrix` | Grid — designed for radio/checkbox. **Textbox `inputType` stores but renders empty cells — avoid for text grids.** |
| `control_widget` | Third-party widget iframe. Works when configured correctly (see below). |

---

## Configurable List Widget — Correct Setup

The Configurable List widget **does work via API** when configured with the right parameters. The key issue before was using `widgetCode` — the correct parameter is `selectedField`.

### Working question properties (reverse-engineered from form builder):

```python
{
    "type":           "control_widget",
    "text":           "Actions",
    "order":          "6",
    "name":           "actions",
    "required":       "Yes",                        # or "No"

    # Core widget identifiers
    "selectedField":  "533946093c1ad0c45d000071",   # NOT widgetCode — ends in 71 not 70
    "frameSrc":       "https://widgets.jotform.io/configurableList/index.html",
    "finalSrc":       "https://widgets.jotform.io/configurableList/index.html",
    "widgetType":     "field",

    # Fields config — one per line, prefix * for required, format: Label:type:
    "fields":         "*Action Description:textarea:\n*Assigned Person:text:\n*Due Date:dateInput:",

    # Row settings
    "minRowsNumber":  "1",
    "limit":          "10",                         # 0 = unlimited

    # Button labels
    "labelAdd":       "+ Add Action",
    "labelRemove":    "x",

    # Layout
    "isTableView":    "undefined",                  # "true" for single-line-per-row layout
    "label":          "Yes",
    "frameWidth":     "580",
    "frameHeight":    "50",
    "maxWidth":       "587",

    # Required meta
    "settingNames":   "fields,minRowsNumber,limit,customCSS,labelAdd,labelRemove,isTableView",
    "widgetTabs":     '[[\"general\",\"settingNames\"],[\"customcss\",\"settingNamesCSS\"]]',
    "shrink":         "No",
    "static":         "No",
    "newLine":        "No",
    "hidden":         "No",
    "theme":          "default",
    "boxAlign":       "Left",
}
```

### Field type options for `fields` config:
- `text` — single-line input
- `textarea` — multi-line input
- `dateInput` — date picker
- `timeInput` — time picker
- `number` — numeric input
- `dropdown: opt1, opt2, opt3` — dropdown
- `radio: opt1, opt2` — radio buttons
- Prefix `*` to make a field required: `*Description:text:`

### widgetCode vs selectedField
- `widgetCode: 533946093c1ad0c45d000070` — **wrong**, renders as empty div
- `selectedField: 533946093c1ad0c45d000071` — **correct**, renders working iframe

---

## Styling Best Practices (from production form)

### Theme setup
- Use `defaultTheme: "v2"` (not v1)
- Apply `styles: "nova"` for the modern nova base theme
- Set `themeID: "5e6b428acc8c4e222d1beb91"` (the standard clean theme)
- Set `v4: "1"` for v4 rendering
- Enable `highlightLine: "Enabled"` for row focus effect

### Recommended properties

```python
{
    "properties[font]":        "Inter",
    "properties[fontsize]":    "16",
    "properties[fontcolor]":   "#2C3345",
    "properties[background]":  "#FFFFFF",
    "properties[formWidth]":   "752",
    "properties[labelWidth]":  "230",
    "properties[styles]":      "nova",
    "properties[defaultTheme]":"v2",
    "properties[v4]":          "1",
    "properties[highlightLine]":"Enabled",
    "properties[styleJSON]": json.dumps({
        "@fontFamily":    "Inter",
        "@fontSize":      "16",
        "@labelAlign":    "Top",
        "@labelWidth":    "230",
        "@formWidth":     "752",
        "@clrText":       "#2C3345",
        "@selectedScheme":"clr-default",
        "@clrBg":         "#F3F3FE",
        "@clrFrame":      "#FFFFFF",
        "@clrInput":      "#FFFFFF",
        "@clrActive":     "#F1F5FF",
        "@clrErrorBg":    "#FFF4F4",
        "@clrLabel":      "#2C3345",
        "@fontLink":      "//cdn.jotfor.ms/fonts/?family=Inter",
    }),
}
```

### injectCSS rules
- Only works on `LEGACY` (not CARD) forms
- `@import` is **not** supported — use `@fontLink` in `styleJSON` for custom fonts
- Max 20,000 characters
- Target questions by: `li#id_{qid}` (input fields) or `li#cid_{qid}` (headers/wide)
- The nova theme + v2 + Inter already looks modern — custom CSS is often unnecessary

---

## Submit Button
- Use `control_button` field type with a meaningful `text` label (e.g. `"Submit Incident Report"`)
- The button is a separate question, not a form property

---

## Useful Form Properties
| Property | Notes |
|----------|-------|
| `hideMailEmptyFields` | `"enable"` — hides blank fields in notification emails |
| `hideEmptySubmissionFields` | `"Yes"` |
| `highlightLine` | `"Enabled"` — highlights focused row |
| `errorNavigation` | `"Yes"` — auto-scroll to errors |
| `clearFieldOnHide` | `"disable"` |
| `thankYouPageLayout` | `"smallImageUp"` |

---

## Active Forms

| Form ID | Title | Status |
|---------|-------|--------|
| `260431018102035` | Incident Report Form | ENABLED (production reference) |
| `260430768025858` | Incident Report Form | DELETED (original attempt) |

**Reference form:** `260431018102035` — use this as the template/best practice for structure, widget config, and styling.
