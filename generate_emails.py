"""
AI Sales Email Agent — Python Helper Script
Use this to test Claude email generation locally before wiring into n8n.

Setup:
  pip install anthropic pandas

Usage:
  python generate_emails.py
"""

import anthropic
import pandas as pd
import json
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────
CLAUDE_API_KEY = "YOUR_CLAUDE_API_KEY"   # Replace with your key from console.anthropic.com
LEADS_CSV      = "leads_sample.csv"       # Path to your leads sheet (exported CSV)
OUTPUT_FILE    = "generated_emails.json"  # Output file for generated emails

# ─── EMAIL PROMPT ──────────────────────────────────────────────────────────
def build_prompt(name: str, role: str, company: str) -> str:
    return f"""Write a cold email to {name}, who is {role} at {company}.

Rules:
- Max 5 sentences
- Open with a reference to their company
- Mention ONE specific pain point for their role
- End with a soft CTA: suggest a 15-minute call
- Tone: professional but human, not salesy
- Format: first line must be exactly 'Subject: [your subject]' then a blank line then the email body only. No extra commentary."""

# ─── GENERATE EMAIL ────────────────────────────────────────────────────────
def generate_email(client: anthropic.Anthropic, name: str, role: str, company: str) -> dict:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[
            {"role": "user", "content": build_prompt(name, role, company)}
        ]
    )

    raw = message.content[0].text
    lines = raw.strip().split("\n")

    subject = ""
    body_lines = []
    past_subject = False

    for line in lines:
        if not past_subject and line.lower().startswith("subject:"):
            subject = line.replace("Subject:", "").replace("subject:", "").strip()
            past_subject = True
        elif past_subject:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    return {
        "name": name,
        "role": role,
        "company": company,
        "subject": subject,
        "body": body,
        "generated_at": datetime.now().isoformat()
    }

# ─── CLASSIFY REPLY ────────────────────────────────────────────────────────
def classify_reply(client: anthropic.Anthropic, reply_text: str) -> str:
    """
    Classify a reply email as: Interested / Not Interested / Needs Follow-up
    """
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this email reply into exactly ONE of:
- Interested
- Not Interested
- Needs Follow-up

Reply: {reply_text}

Respond with ONLY the classification label, nothing else."""
            }
        ]
    )
    return message.content[0].text.strip()

# ─── MAIN ──────────────────────────────────────────────────────────────────
def main():
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    print(f"Reading leads from {LEADS_CSV}...")
    df = pd.read_csv(LEADS_CSV)
    pending = df[df["Status"] == "pending"]
    print(f"Found {len(pending)} pending leads.\n")

    results = []

    for _, row in pending.iterrows():
        print(f"Generating email for {row['Name']} at {row['Company']}...")
        try:
            email = generate_email(client, row["Name"], row["Role"], row["Company"])
            results.append(email)
            print(f"  Subject: {email['subject']}")
            print(f"  Body preview: {email['body'][:80]}...\n")
        except Exception as e:
            print(f"  ERROR for {row['Name']}: {e}\n")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results)} emails written to {OUTPUT_FILE}")
    print("\nExample classify_reply usage:")
    sample_reply = "Thanks for reaching out! I'd love to find out more, happy to chat."
    classification = classify_reply(client, sample_reply)
    print(f"  Reply: '{sample_reply}'")
    print(f"  Classification: {classification}")

if __name__ == "__main__":
    main()
