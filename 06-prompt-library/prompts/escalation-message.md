---
id: escalation-message
title: Escalation message
category: communication
purpose: Write a short, blame-free escalation with a specific ask and deadline.
variables:
  - name: recipient_role
    description: Who you are escalating to, by role.
  - name: issue
    description: What is wrong, in your own words.
  - name: impact
    description: What happens if nothing changes.
  - name: tried
    description: What you have already done about it.
  - name: ask
    description: The specific decision or help you need.
  - name: deadline
    description: When you need it by.
tips: An escalation works when the ask is specific. If you cannot write the ask in one sentence, work on that before you send anything.
criteria: The message states the issue and impact in the first lines, summarises what has been tried, makes one specific ask with the deadline, offers options where relevant, uses neutral language that does not blame people, and stays under about 120 words.
example:
  recipient_role: Head of Engineering
  issue: The vendor has not confirmed the test environment date, and two requests this month went unanswered.
  impact: Testing cannot start on 3 Feb. Go-live on 14 March is at risk, and that date is a regulatory deadline.
  tried: Weekly vendor calls, two written requests, raised with the vendor account manager on 15 Jan.
  ask: Contact the vendor's senior sponsor to secure a confirmed environment date.
  deadline: Friday 24 Jan
---
Write an escalation message to the {{recipient_role}}.

The issue:
{{issue}}

The impact if nothing changes:
{{impact}}

What I have already tried:
{{tried}}

What I need:
{{ask}}

Needed by: {{deadline}}

Rules:
- Put the issue and the impact in the first two sentences.
- Make one specific ask and include the deadline.
- Use neutral language and do not blame any person or team.
- If there are sensible alternatives, offer up to two as options.
- Keep it under 120 words.
