---
id: risk-log-review
title: Risk log review
category: risk
purpose: Review a pasted risk log for weak entries, gaps and the risks that most need escalation.
variables:
  - name: risk_log
    description: The risk log pasted as a table or list.
  - name: project_context
    description: Two or three sentences on the project and its current phase.
tips: Works best on 10 to 40 risks. For longer logs, review one category at a time.
criteria: The review identifies specific weak entries by id, covering vague statements, missing owners or dates, inconsistent scoring, duplicates and risks without mitigation, names no more than three risks to escalate with reasons, points out categories that look missing given the context, and does not rewrite the whole log.
example:
  risk_log: |
    R1 | Vendor delay | L4 I4 | Owner: TBC | Mitigation: monitor
    R2 | Data quality in legacy system may cause migration failures | L3 I5 | Owner: Data lead | Mitigation: profiling and cleansing sprint, due 5 Feb
    R3 | Resourcing | L2 I2 | Owner: PM | Mitigation: none
    R4 | Vendor environment late | L4 I4 | Owner: PM | Mitigation: weekly checkpoint with vendor
  project_context: Payments platform migration, now in the testing phase, go-live fixed for 14 March by a regulatory deadline.
---
Review this risk log as an experienced delivery manager would.

Project context:
{{project_context}}

<risk_log>
{{risk_log}}
</risk_log>

Report on:
1. Weak entries: refer to each by id and say what is wrong (vague wording, no owner, no date, no mitigation, scoring that looks inconsistent).
2. Possible duplicates or overlaps.
3. Top 3 risks to escalate now, with one sentence each on why.
4. Risk categories that look missing for this project and phase.

Rules:
- Quote ids exactly as they appear.
- Do not rewrite the whole log. Suggest a fix only for the top 3 weakest entries.
- If you cannot judge something from what is given, say so.
