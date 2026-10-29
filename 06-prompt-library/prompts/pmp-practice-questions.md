---
id: pmp-practice-questions
title: PMP-style practice questions
category: learning
purpose: Generate original scenario-based practice questions on a topic, with explained answers.
variables:
  - name: topic
    description: What to practise, for example "stakeholder engagement", "risk response" or "agile delivery".
  - name: count
    description: How many questions.
  - name: difficulty
    description: For example "foundation", "intermediate" or "hard".
    required: false
    default: intermediate
tips: These are original practice items, not real exam questions. Check the explanations against your study material, and treat the model as a study partner rather than the authority.
criteria: Each question is an original workplace scenario with four options and one best answer, the answer key explains why the correct option is best and why each other option is weaker, difficulty matches the request, and the questions do not reproduce real exam content.
example:
  topic: risk response
  count: 2
  difficulty: intermediate
---
Write {{count}} original multiple-choice practice questions on {{topic}} at {{difficulty}} difficulty, in the style of scenario-based project management exam questions.

For each question:
- A short workplace scenario of two to four sentences.
- Four options labelled A to D, with exactly one best answer.
- Wrong options should be plausible, not silly.

After all questions, give an answer key. For each question, say which option is best, why it is best, and in one sentence why each other option is weaker.

Rules:
- Write original questions. Do not reproduce questions from any real exam or published question bank.
- Vary which letter is correct.
- If you are unsure about a point of practice, say so in the explanation.
