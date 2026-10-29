# Reading list and repos to explore

Order is a suggestion: read the first three, then build, then dip into the repos.
Links were checked in web search results when this list was made; pages may move.

## Read (Anthropic)

1. Building effective agents – https://www.anthropic.com/engineering/building-effective-agents
2. Writing effective tools for agents – https://www.anthropic.com/engineering/writing-tools-for-agents
3. Effective context engineering for agents – https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
4. How we built our multi-agent research system – https://www.anthropic.com/engineering/multi-agent-research-system
5. Demystifying evals for AI agents – https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
6. Tool use docs – https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview

## Learn (courses)

- Hugging Face Agents Course – https://huggingface.co/learn/agents-course
- Microsoft AI Agents for Beginners – https://github.com/microsoft/ai-agents-for-beginners

## Protocols

- Model Context Protocol intro – https://modelcontextprotocol.io/introduction
- MCP Python SDK – https://github.com/modelcontextprotocol/python-sdk

## Repos to explore (read the code, run an example)

| Repo | Why |
|------|-----|
| https://github.com/langchain-ai/langgraph | Agents as graphs; state, branching, human-in-the-loop |
| https://github.com/huggingface/smolagents | Tiny agent library; compare its loop with `loop.py` |
| https://github.com/openai/openai-agents-python | Handoffs, guardrails, tracing |
| https://github.com/anthropics/claude-agent-sdk-python | Claude's agent SDK for Python |
| https://github.com/anthropics/claude-cookbooks | Tool use and agent recipes |

## Connected material in this repo

- `../02-ai-eval-toolkit` – test an agent's output (see `evals/`)
- `../05-learning-map` – full visual learning route with free resources
- `../06-prompt-library` – prompts for delivery management you can feed to an agent
