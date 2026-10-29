---
id: meeting-actions
title: Meeting decisions and actions
category: meetings
purpose: Turn meeting notes into decisions, actions with owners and dates, and open questions.
variables:
  - name: meeting_date
    description: Date of the meeting.
  - name: notes
    description: Raw notes or a rough transcript.
  - name: attendees
    description: Attendees by role or initials, if you want owners matched.
    required: false
    default: Not provided
tips: Send the output to attendees quickly while the meeting is fresh. Actions with no owner or date are flagged so you can chase them.
criteria: The answer lists decisions separately from actions, gives each action an owner and due date only when the notes state them, flags actions missing an owner or date, lists open questions, and does not assign owners or dates that were not in the notes.
example:
  meeting_date: 21 Jan
  attendees: PM, test lead, data lead, vendor rep
  notes: |
    Agreed to run the two test phases in parallel. Data lead will share the failing-record analysis by Wednesday.
    Someone needs to ask finance about UAT sign-off timing. Vendor rep to confirm the environment date, no date given.
    Open point: do we have budget for 2 extra testers?
---
Summarise this meeting.

Date: {{meeting_date}}
Attendees: {{attendees}}

<notes>
{{notes}}
</notes>

Produce three sections:
1. Decisions: what was agreed, one line each.
2. Actions: a table with action, owner and due date.
3. Open questions: things raised but not resolved.

Rules:
- Only record an owner or due date if the notes state it. Otherwise write "Not stated".
- After the table, list the actions that have no owner or no date, so I can chase them.
- Do not add decisions or actions that are not in the notes.
- Keep it to one page.
