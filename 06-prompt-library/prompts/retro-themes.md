---
id: retro-themes
title: Retrospective themes
category: team
purpose: Group raw retrospective feedback into themes and propose a few measurable experiments.
variables:
  - name: period
    description: The sprint, release or phase being reviewed.
  - name: feedback
    description: Raw retrospective notes or sticky-note text.
tips: Remove names from the feedback before using an AI tool. Pick one or two experiments with the team rather than trying all of them.
criteria: The answer groups feedback into three to five themes with a rough count of supporting comments, separates what went well from what to change, proposes up to three experiments each with an owner by role and a way to measure it, avoids naming individuals, and does not invent feedback.
example:
  period: Sprint 14
  feedback: |
    Stand-ups run too long. Good teamwork on the migration bug. Requirements changed mid-sprint again. Test environment was down for two days.
    Stand-ups too long. Loved the pairing sessions. Unclear who approves scope changes. Environment problems slowed testing.
    We should demo more often. Scope changes keep coming in without notice.
---
Analyse the retrospective feedback for {{period}}.

<feedback>
{{feedback}}
</feedback>

Produce:
1. Three to five themes, each with the number of comments that support it.
2. What went well, in two or three bullets.
3. What to change, in two or three bullets.
4. Up to three experiments for next period. For each: what to try, an owner by role, and how we will know it worked.

Rules:
- Do not name individuals.
- Use only the feedback above. Do not add comments that are not there.
- If a theme has only one comment, say so.
