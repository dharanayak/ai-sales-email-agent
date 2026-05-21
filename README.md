# 🤖 AI Sales Email Agent

> **Agentic AI system** that autonomously generates hyper-personalised sales emails, sends them, reads replies, classifies them with AI, and triggers follow-up sequences — with zero human effort.

![Status](https://img.shields.io/badge/Status-Fully%20Working-27AE60?style=flat-square)
![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-EA4B71?style=flat-square)
![Claude](https://img.shields.io/badge/Claude%20API-AI%20Engine-8B5CF6?style=flat-square)
![Gmail](https://img.shields.io/badge/Gmail%20API-Email%20Dispatch-D93025?style=flat-square)
![PowerBI](https://img.shields.io/badge/Power%20BI-KPI%20Dashboard-F2C811?style=flat-square)

---

## 📌 What This Project Does

| Capability | Description |
|---|---|
| ✉️ **Auto-generate emails** | Claude API writes a unique personalised email for every lead — not a template |
| 📤 **Auto-send emails** | n8n + Gmail API dispatches emails daily at 9 AM, zero manual effort |
| 🧠 **Summarise replies with AI** | Claude classifies every reply: Interested / Not Interested / Needs Follow-up |
| 🔁 **Auto follow-up** | Triggers contextual follow-up sequences based on recipient reply behaviour |
| 📊 **KPI Dashboard** | Power BI tracks send volume, reply rate, follow-up conversion in real time |

---

## 🧰 Tech Stack

| Tool | Role |
|------|------|
| **n8n** | Workflow automation engine — orchestrates all steps |
| **Claude API** | Writes personalised emails + classifies replies |
| **Gmail API** | Sends emails + reads inbox for replies (OAuth2) |
| **Google Sheets** | Lead database (Name, Company, Role, Email, Status) |
| **Notion API** | CRM log — records every action and reply outcome |
| **Power BI** | Live dashboard — send volume, reply rate, conversion KPIs |

---

## 🔄 Agentic Workflow Architecture

```
Google Sheet (leads: pending)
        │
        ▼
n8n Schedule Trigger (9 AM daily)
        │
        ▼
Read leads → Valid Email? ──NO──► Skip row
        │ YES
        ▼
Claude API — Write personalised email
        │
        ▼
Parse: Subject + Body
        │
        ▼
Gmail API — Send email
        │
   ┌────┴─────────────────────┐
   ▼                          ▼
Update Sheet              Gmail Inbox Watch
(Status = sent)           (trigger on reply)
                               │
                               ▼
                      Claude API — Classify reply
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
               Interested  Not          Needs
               → CRM ping  Interested   Follow-up
                           → Close      → Schedule
                                          next email
```

---

## 📁 Repository Structure

```
ai-sales-email-agent/
├── workflow/
│   └── sales_email_agent.json      ← Import this into n8n
├── code/
│   └── generate_emails.py          ← Python test script (local)
├── data/
│   └── leads_sample.csv            ← Sample Google Sheet structure
├── docs/
│   ├── AI_Sales_Email_Agent_ProjectDoc.pdf   ← Full project document
│   └── workflow_flowchart.svg      ← Architecture flowchart
└── README.md
```

---

## ⚡ Quick Setup (3 steps)

### 1 — Install n8n
```bash
npm install -g n8n
npx n8n
# Opens at http://localhost:5678
```

### 2 — Import the workflow
1. Open n8n → **Workflows** → **Import from file**
2. Upload `workflow/sales_email_agent.json`

### 3 — Add your credentials

| Credential | Where to get it |
|---|---|
| Claude API Key | [console.anthropic.com](https://console.anthropic.com) → API Keys |
| Google Sheets OAuth2 | Google Cloud Console → Enable Sheets API |
| Gmail OAuth2 | Google Cloud Console → Enable Gmail API |
| Notion API | [notion.so/my-integrations](https://www.notion.so/my-integrations) |

Replace `YOUR_GOOGLE_SHEET_ID` in the workflow with your actual Sheet ID from the URL.

---

## 🗂️ Google Sheet Structure

| Name | Company | Role | Email | Status | SentDate | Subject | ReplyType |
|------|---------|------|-------|--------|----------|---------|-----------|
| John Smith | Acme Corp | CTO | john@acme.com | pending | | | |

Set `Status = pending` for any lead you want emailed. The agent skips rows already marked `sent`.

---

## 🧠 Claude Prompt Used

```
Write a cold email to {{Name}}, who is {{Role}} at {{Company}}.

Rules:
- Max 5 sentences
- Open with a reference to their company
- Mention ONE specific pain point for their role
- End with a soft CTA: suggest a 15-minute call
- Tone: professional but human, not salesy
- Format: Subject: [subject line] then blank line then body only
```

**Reply classification prompt:**
```
Classify this email reply as exactly one of:
Interested / Not Interested / Needs Follow-up
Respond with ONLY the label.
```

---

## 📊 Sample Power BI KPIs

- **Emails sent** per day / week / campaign
- **Reply rate** — % of leads who replied
- **Classification breakdown** — Interested vs Not Interested vs Follow-up
- **Follow-up conversion** — % of Follow-ups that became Interested

---

## 📜 License

MIT — free to use, modify, and build on.

---

## 👤 Author

**Dhara_Nayak**
[Portfolio](https://github.com/dharanayak/)

> Part of a Gen AI & Agentic AI portfolio. See my other projects on my profile.
