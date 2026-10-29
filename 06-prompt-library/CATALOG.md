# Prompt catalog

12 prompts for delivery management. Each links to its file, which holds the full prompt, an example and tips.

To fill one: `python -m promptlib fill <id> --example`, or supply your own values with `--var name=value`.

## Communication

| Prompt | What it does | Inputs |
|---|---|---|
| [Escalation message](prompts/escalation-message.md) (`escalation-message`) | Write a short, blame-free escalation with a specific ask and deadline. | `recipient_role`, `issue`, `impact`, `tried`, `ask`, `deadline` |
| [Stakeholder update email](prompts/stakeholder-update-email.md) (`stakeholder-update-email`) | Draft a short update email that leads with the bottom line and ends with a clear ask. | `audience`, `situation`, `key_message`, `ask (optional)`, `tone (optional)` |

## Learning

| Prompt | What it does | Inputs |
|---|---|---|
| [PMP-style practice questions](prompts/pmp-practice-questions.md) (`pmp-practice-questions`) | Generate original scenario-based practice questions on a topic, with explained answers. | `topic`, `count`, `difficulty (optional)` |

## Meetings

| Prompt | What it does | Inputs |
|---|---|---|
| [Meeting decisions and actions](prompts/meeting-actions.md) (`meeting-actions`) | Turn meeting notes into decisions, actions with owners and dates, and open questions. | `meeting_date`, `notes`, `attendees (optional)` |

## Planning

| Prompt | What it does | Inputs |
|---|---|---|
| [Delay or change impact assessment](prompts/delay-impact-assessment.md) (`delay-impact-assessment`) | Assess what a delay or change request does to scope, schedule, cost, quality and risk, and compare options. | `change`, `baseline`, `constraints` |
| [RAID items from notes](prompts/raid-from-notes.md) (`raid-from-notes`) | Pull risks, assumptions, issues and dependencies out of messy meeting or workshop notes. | `project`, `notes` |

## Privacy

| Prompt | What it does | Inputs |
|---|---|---|
| [Redaction check](prompts/redaction-check.md) (`redaction-check`) | Find personal and confidential details in text so you can remove them before sharing it elsewhere. | `text` |

## Reporting

| Prompt | What it does | Inputs |
|---|---|---|
| [Steering committee brief](prompts/steering-committee-brief.md) (`steering-committee-brief`) | Compress project status into a one-page brief that asks for specific decisions. | `project`, `status_inputs`, `decisions_needed`, `audience_notes (optional)` |
| [Weekly status report](prompts/weekly-status-report.md) (`weekly-status-report`) | Turn raw weekly notes into a short RAG status report for a chosen audience. | `project`, `period`, `audience`, `updates`, `metrics (optional)` |

## Risk

| Prompt | What it does | Inputs |
|---|---|---|
| [Risk log entry](prompts/risk-log-entry.md) (`risk-log-entry`) | Turn a vague worry into a well-formed risk register entry with scoring and responses. | `concern`, `project_context`, `existing_risks (optional)` |
| [Risk log review](prompts/risk-log-review.md) (`risk-log-review`) | Review a pasted risk log for weak entries, gaps and the risks that most need escalation. | `risk_log`, `project_context` |

## Team

| Prompt | What it does | Inputs |
|---|---|---|
| [Retrospective themes](prompts/retro-themes.md) (`retro-themes`) | Group raw retrospective feedback into themes and propose a few measurable experiments. | `period`, `feedback` |
