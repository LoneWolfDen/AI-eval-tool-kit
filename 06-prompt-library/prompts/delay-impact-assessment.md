---
id: delay-impact-assessment
title: Delay or change impact assessment
category: planning
purpose: Assess what a delay or change request does to scope, schedule, cost, quality and risk, and compare options.
variables:
  - name: change
    description: The delay or change being considered.
  - name: baseline
    description: Current plan in brief, such as scope, key dates and budget.
  - name: constraints
    description: Fixed points, such as regulatory dates, budget ceiling or team size.
tips: The model does not know your critical path. Ask it to list assumptions, then correct them before you rely on the result.
criteria: The assessment covers scope, schedule, cost, quality and risk, states its assumptions explicitly, offers two or three options with trade-offs, makes a recommendation with a reason, names the information that would change the recommendation, and does not invent figures that were not provided.
example:
  change: The vendor test environment will be 3 weeks late.
  baseline: Go-live 14 March. Testing 3 Feb to 14 Mar in two phases. Budget 1.2m, 62% spent. Test team of 6.
  constraints: The 14 March date is a regulatory deadline. Budget cannot exceed 1.3m without board approval.
---
Assess the impact of this change on my project.

The change:
{{change}}

Current plan:
{{baseline}}

Constraints:
{{constraints}}

Provide:
1. Impact on scope, schedule, cost, quality and risk, one short paragraph or bullet group each.
2. Your assumptions, listed explicitly. Mark any that I should confirm.
3. Two or three options, each with its trade-offs.
4. A recommendation and the main reason for it.
5. What information would change your recommendation.

Rules:
- Use only the numbers given. If a figure is needed and not provided, say "needs estimate" instead of guessing.
- Keep it under 400 words.
