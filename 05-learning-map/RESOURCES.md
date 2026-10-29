# AI learning route

From prompting basics to team guidance: evaluation, agents and privacy, using free resources.

Links were checked on 2026-10-29. Pages move, so edit `resources.json` and run `python build.py` to refresh this file.

## Prompting basics

Get reliable answers from a model by writing clear prompts. Everything later builds on this.

**Start here**

- [Interactive prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) (repo, Free): Hands-on notebooks that teach prompting one technique at a time.
- [Anthropic courses](https://github.com/anthropics/courses) (repo, Free): Anthropic's educational courses, including one on real-world prompting.

**Stage gate: build it.** Write five prompts for tasks you do every week, such as a status summary, risk wording or a stakeholder reply. Note what makes each answer better or worse.

**Check yourself.** Can you say in one sentence why a clearer prompt gave a better answer?

## AI evaluation

Measure whether an AI answer is good, with repeatable tests instead of gut feel.

**Start here**

- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/build-with-claude/develop-tests) (read, Free): Anthropic's guide to writing measurable success criteria and test cases.
- [Your AI product needs evals](https://hamel.dev/blog/posts/evals/index.html) (read, Free): A practitioner's essay on building evals for an AI product.
- [Evaluating AI agents (DeepLearning.AI)](https://www.deeplearning.ai/courses/evaluating-ai-agents) (course, Free to enrol during the platform beta. The graded assignment and certificate need a paid membership.): Beginner short course built with Arize AI: about 2.5 hours, 15 video lessons, basic Python needed.
- [Inspect AI tutorial](https://inspect.aisi.org.uk/tutorial.html) (course, Free): Write and run your first eval with the UK AI Security Institute's framework.
- [Your own toolkit: 02-ai-eval-toolkit](../02-ai-eval-toolkit/README.md) (repo, Yours): The modular Python toolkit from this repo. Extend it as you learn.

**Go deeper**

- [AI evals: everything you need to know](https://hamel.dev/blog/posts/evals-faq/) (read, Free): Hamel Husain and Shreya Shankar answer common eval questions, such as how many examples you need.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (read, Free): Anthropic's engineering write-up on evaluating agents.
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) (repo, Free): Open-source framework for LLM evaluations from the UK AI Security Institute.
- [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals) (repo, Free): A collection of ready-made evals for Inspect AI. Good for reading how others write them.
- [promptfoo](https://github.com/promptfoo/promptfoo) (repo, Free): Tests prompts, agents and RAG setups, and also does red teaming. Declarative configs, command line and CI support.
- [DeepEval](https://github.com/confident-ai/deepeval) (repo, Free): Python framework for evaluating LLM outputs.
- [Ragas](https://github.com/explodinggradients/ragas) (repo, Free): Evaluation toolkit for LLM applications, known for retrieval-augmented generation (RAG) checks.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) (repo, Free): Framework for evaluating language models on standard academic benchmarks.
- [OpenAI Evals](https://github.com/openai/evals) (repo, Free): A framework for evaluating LLMs, plus an open-source registry of benchmarks.

**Stage gate: build it.** Write a 10-case suite from your own work, run it on two models, and compare them in the HTML report from your toolkit.

**Check yourself.** Which of your checks would let a wrong answer pass? Which would fail a right one?

## Agents

Understand how models use tools to complete multi-step tasks, and when a simple workflow is the better choice.

**Start here**

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) (read, Free): Anthropic's guide to agent design patterns.
- [Hugging Face AI agents course](https://huggingface.co/learn/agents-course) (course, Free, including the certificate): Theory to hands-on building, with smolagents, LlamaIndex and LangGraph. Units, three bonus units and an optional certificate.
- [AI agents for beginners (Microsoft)](https://github.com/microsoft/ai-agents-for-beginners) (repo, Free): A lesson-by-lesson open course with code samples.
- [What is the Model Context Protocol?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro) (read, Free): The open protocol for connecting AI apps to tools and data.

**Go deeper**

- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (read, Free): How to design the tools an agent calls.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (read, Free): How to manage what an agent sees as its task grows.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (read, Free): A real multi-agent system, described by the team that built it.
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/) (repo, Free): Documentation for building your own MCP server in Python.

**Stage gate: build it.** Build a small agent with two or three tools, for example one that reads a risk log and drafts a status note. Then add test cases for it to your eval suite.

**Check yourself.** When would a fixed workflow beat an agent for this task?

## Privacy and security

Know what personal data can reach an AI tool, what the law expects, and how models get attacked.

**Start here**

- [ICO guidance on AI and data protection](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/about-this-guidance/) (guidance, Free): The UK regulator's guidance on applying data protection law to AI.
- [OWASP Top 10 for LLM applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (guidance, Free): The standard list of security risks for LLM applications, such as prompt injection.
- [Microsoft Presidio](https://github.com/microsoft/presidio) (repo, Free): Open-source tool that finds and masks personal data in text, images and structured data.

**Go deeper**

- [ICO: explaining decisions made with AI](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/explaining-decisions-made-with-artificial-intelligence/part-1-the-basics-of-explaining-ai/) (guidance, Free): How to explain AI-assisted decisions to the people they affect.
- [ICO audit toolkit: governance and accountability in AI](https://ico.org.uk/for-organisations/advice-and-services/audits/data-protection-audit-framework/toolkits/artificial-intelligence/governance-and-accountability-in-ai/) (guidance, Free): A checklist-style view of what good AI governance looks like to an auditor.
- [NCSC guidelines for secure AI system development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) (guidance, Free): UK National Cyber Security Centre guidelines, developed with international partners.
- [Presidio documentation](https://microsoft.github.io/presidio) (read, Free): Getting started and reference for detecting and anonymising personal data.

**Stage gate: build it.** Add a privacy red-team suite to your toolkit: prompts that try to pull out personal data or hidden instructions. Try Presidio as a stronger replacement for the no_pii check.

**Check yourself.** What personal data could reach an AI tool in your team's daily work, and where does it go next?

## Governance and team guidance

Turn what you have learned into rules your team can follow without asking you each time.

**Start here**

- [AI playbook for the UK government](https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government) (guidance, Free): Written for the UK public sector, and a good template for the principles any team needs.
- [NIST AI risk management framework](https://www.nist.gov/itl/AI-risk-management-framework) (guidance, Free): A voluntary framework from the US standards body for managing AI risk.

**Go deeper**

- [NIST generative AI profile (AI 600-1)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) (guidance, Free): A companion profile that applies the framework to generative AI.
- [OWASP GenAI security project](https://owasp.org/www-project-genai-security/) (guidance, Free): OWASP's wider project on generative AI security, beyond the top 10 list.

**Stage gate: build it.** Draft a one-page AI use guideline for your team: what data may go into AI tools, who approves new uses, and how outputs are checked.

**Check yourself.** Could a new team member follow it without asking you anything?
