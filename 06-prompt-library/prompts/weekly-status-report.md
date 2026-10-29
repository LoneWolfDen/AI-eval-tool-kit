---
id: weekly-status-report
title: Weekly status report
category: reporting
purpose: Turn raw weekly notes into a short RAG status report for a chosen audience.
variables:
  - name: project
    description: Project name.
  - name: period
    description: Reporting period, for example "Week ending 23 Jan".
  - name: audience
    description: Who will read it, for example "Programme board" or "Delivery team".
  - name: updates
    description: Your raw notes for the period. Messy is fine.
  - name: metrics
    description: Any numbers worth including, such as velocity, budget spent or defects.
    required: false
    default: None provided
tips: Paste real notes, not a polished summary. Remove names and client details before using an AI tool you have not been cleared to use.
criteria: The report states Green, Amber or Red with a one-sentence reason, keeps progress and next steps to a few bullets each, lists risks with an owner and action, says what help is needed, stays under about 300 words, and marks missing information as "Not provided" instead of inventing it.
example:
  project: Project Kestrel
  period: Week ending 23 Jan
  audience: Programme board
  updates: |
    Payments API integration finished testing, 2 minor defects left. Data migration dry run 1 done, found 3% of records failing validation.
    Vendor still has not confirmed the March environment date. Two engineers on leave next week. UAT scripts reviewed, sign-off pending from finance.
  metrics: |
    Budget spent 62% against 58% planned. 41 of 60 test cases passed.
---
You are helping a technology delivery manager write a weekly status report.

Project: {{project}}
Reporting period: {{period}}
Audience: {{audience}}

<raw_updates>
{{updates}}
</raw_updates>

<metrics>
{{metrics}}
</metrics>

Write the report using only the information above.

Format:
1. Overall status: Green, Amber or Red, with one sentence of justification.
2. Progress this period: up to 5 bullets that describe outcomes, not activities.
3. Planned next period: up to 5 bullets.
4. Risks and issues: each with its impact, an owner and the action in progress.
5. Decisions or help needed: what is needed, from whom and by when.

Rules:
- Match tone and level of detail to the audience.
- If the status is not stated in the updates, propose one and say it is your proposal.
- If something is missing, write "Not provided". Do not invent dates, names or numbers.
- Keep the whole report under 300 words.
