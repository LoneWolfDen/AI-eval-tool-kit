---
id: raid-from-notes
title: RAID items from notes
category: planning
purpose: Pull risks, assumptions, issues and dependencies out of messy meeting or workshop notes.
variables:
  - name: project
    description: Project name.
  - name: notes
    description: Raw notes from a meeting or workshop.
tips: Review the output against your notes. The model can misfile an issue as a risk, so check the Uncertain section first.
criteria: The answer sorts items into risks, assumptions, issues and dependencies, distinguishes things that have already happened (issues) from things that might happen (risks), attaches a short supporting phrase from the notes to each item, puts doubtful items in an Uncertain section, and invents nothing that is not in the notes.
example:
  project: Project Kestrel
  notes: |
    Finance said UAT sign-off will probably take two weeks, not one. We assume the vendor environment is ready by 20 Feb.
    The payments API team has not delivered the updated spec yet, which blocks the mapping work. A few people worried that data from the old system might not validate.
    The test lead is already short of two testers this sprint.
---
Extract RAID items for project {{project}} from these notes.

<notes>
{{notes}}
</notes>

Sort what you find into four groups:
- Risks: something that might happen.
- Assumptions: something we are treating as true without proof.
- Issues: something that has already happened and needs action.
- Dependencies: something we need from another team or party.

Rules:
- For each item give a short title and a short supporting phrase copied from the notes.
- If an item could fit two groups, choose the best one and add it to an "Uncertain" section with a one-line reason.
- Do not add items that are not supported by the notes.
- Present each group as a table with the columns: title, supporting phrase.
