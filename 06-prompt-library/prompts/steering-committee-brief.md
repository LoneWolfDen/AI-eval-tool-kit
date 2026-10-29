---
id: steering-committee-brief
title: Steering committee brief
category: reporting
purpose: Compress project status into a one-page brief that asks for specific decisions.
variables:
  - name: project
    description: Project name.
  - name: status_inputs
    description: "Everything you know about status: progress, budget, risks, people and milestones."
  - name: decisions_needed
    description: The decisions you want the committee to make.
  - name: audience_notes
    description: Anything about the committee that shapes the brief, such as what they care about.
    required: false
    default: None provided
tips: Start with the decisions you need. If the brief does not lead to a decision, it may be a report rather than a brief.
criteria: The brief opens with a one-line headline, rates scope, schedule, budget, risk and people, lists the top three risks, presents each requested decision with options and a recommendation, outlines the next 30 days, stays under about 350 words, and uses only the information provided.
example:
  project: Project Kestrel
  status_inputs: |
    Build complete. Testing starts late because the vendor environment is 3 weeks behind. Budget 62% spent against 58% planned.
    Top risks: vendor environment, data quality, UAT sign-off timing. Team morale steady, two engineers leaving in April.
  decisions_needed: |
    Approve 2 extra testers for 4 weeks. Agree to escalate the vendor delay to their senior sponsor.
  audience_notes: Committee cares most about the regulatory date and budget.
---
Prepare a one-page steering committee brief for {{project}}.

<status_inputs>
{{status_inputs}}
</status_inputs>

Decisions I need from the committee:
{{decisions_needed}}

About the audience:
{{audience_notes}}

Format:
1. Headline: one line.
2. Status: scope, schedule, budget, risk and people, each rated Green, Amber or Red with a few words of reason.
3. Top three risks.
4. Decisions requested: for each, the options and your recommendation.
5. Next 30 days: up to four bullets.

Rules:
- Use only the information above. Write "Not provided" where something is missing.
- Keep the whole brief under 350 words.
