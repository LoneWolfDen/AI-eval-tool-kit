---
id: stakeholder-update-email
title: Stakeholder update email
category: communication
purpose: Draft a short update email that leads with the bottom line and ends with a clear ask.
variables:
  - name: audience
    description: Who it is for and their level, for example "Sponsor, senior, little time".
  - name: situation
    description: What has happened or changed, in your own words.
  - name: key_message
    description: The one thing the reader must take away.
  - name: ask
    description: What you need from them, if anything.
    required: false
    default: Nothing. This is for information.
  - name: tone
    description: Tone to use, for example "calm and factual" or "warm but direct".
    required: false
    default: calm and factual
tips: Give the model the situation and the one key message. If you do not know the key message yet, that is the thing to work out first.
criteria: The email opens with the bottom line, includes a subject line, stays under about 150 words, states the ask clearly with a date when one is given, uses the requested tone, and does not add facts that were not provided.
example:
  audience: Project sponsor, senior, has two minutes
  situation: The vendor environment will be 3 weeks late. We can recover 1 week by running two test phases in parallel, which needs 2 extra testers.
  key_message: Go-live moves from 14 March to 28 March unless we add testers.
  ask: Approve 2 extra testers for 4 weeks by Friday.
  tone: calm and factual
---
Write an email to this audience: {{audience}}

What has happened:
{{situation}}

The one message they must remember:
{{key_message}}

What I need from them:
{{ask}}

Tone: {{tone}}

Rules:
- Start with the bottom line in the first sentence.
- Include a subject line that states the point.
- Keep the body under 150 words.
- State the ask in its own short paragraph, with the date it is needed by if one was given.
- Do not add facts, dates or numbers that are not above.
