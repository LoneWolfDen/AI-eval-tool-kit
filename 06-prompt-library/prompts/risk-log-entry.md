---
id: risk-log-entry
title: Risk log entry
category: risk
purpose: Turn a vague worry into a well-formed risk register entry with scoring and responses.
variables:
  - name: concern
    description: The worry in plain words, as you would say it to a colleague.
  - name: project_context
    description: Two or three sentences on the project, timeline and constraints.
  - name: existing_risks
    description: Titles of risks already logged, so the model can flag overlap.
    required: false
    default: None provided
tips: The model proposes scores and owners as a starting point. You and the team decide the final likelihood, impact and owner.
criteria: The answer states the risk as cause, event and impact, proposes likelihood and impact scores from 1 to 5 with a short reason and the multiplied score, recommends a response type with concrete actions, lists early-warning triggers, suggests an owner by role rather than by name, flags any overlap with existing risks, and lists open questions instead of guessing.
example:
  concern: The vendor keeps being vague about when our test environment will be ready and I think it will slip.
  project_context: Payments platform migration with a fixed go-live of 14 March tied to a regulatory deadline. Testing needs the vendor environment for 6 weeks.
  existing_risks: Key engineer attrition; Data quality in legacy system
---
Help me write a risk register entry.

My concern, in my own words:
{{concern}}

Project context:
{{project_context}}

Risks already in the log:
{{existing_risks}}

Produce:
1. Risk statement in the form "If [cause], then [event], resulting in [impact]".
2. Likelihood (1 to 5) and impact (1 to 5), each with a one-sentence reason, then the score (likelihood x impact).
3. Recommended response: avoid, mitigate, transfer or accept, with 2 to 4 concrete actions.
4. Early-warning indicators that would show the risk is becoming real.
5. A suggested owner by role, not by name.
6. Whether this overlaps with an existing risk.
7. Up to 3 questions I should answer to firm this up.

Rules:
- Do not state facts about the project that I did not give you. Where you assume something, say so.
- Keep each section brief.
