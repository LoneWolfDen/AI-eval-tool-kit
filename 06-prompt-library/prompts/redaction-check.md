---
id: redaction-check
title: Redaction check
category: privacy
purpose: Find personal and confidential details in text so you can remove them before sharing it elsewhere.
variables:
  - name: text
    description: The text to check.
tips: Run this with a local model or a tool your organisation has approved, since the text still contains the sensitive details. Then redact, and read the redacted version yourself before sharing it.
criteria: The answer lists personal and confidential items by category, identifies each with a short fragment and its location, includes a redacted copy that uses consistent placeholders such as [PERSON_1], states what it could not judge, and does not add information that is not in the text.
example:
  text: |
    Hi Priya, as discussed with Marcus Webb (marcus.webb@example.com, 07700 900123), the Kestrel budget overrun is 120k.
    Please send the invoice to 14 Oak Lane, Leeds, and quote contract ref KST-2291. The client, Northfield Bank, has not agreed yet.
---
Check the text below for personal or confidential details before it is shared outside its original audience.

<text>
{{text}}
</text>

Do three things:
1. List what you find, grouped by category: names, email addresses, phone numbers, addresses, identifiers and reference numbers, financial figures, client or project names, credentials or keys. For each item give a short fragment and say where it appears.
2. Produce a redacted copy of the text. Replace each item with a consistent placeholder such as [PERSON_1], [EMAIL_1], [CLIENT_1], so the same item always gets the same placeholder.
3. Say what you could not judge, for example details that only the author can say are confidential.

Rules:
- Do not add information that is not in the text.
- When unsure whether something is sensitive, include it and mark it "unsure".
