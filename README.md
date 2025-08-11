## Puzzle Workshop: Building Practical Agents with LangChain and MCP

This hands-on guide walks you through the Puzzle Agent project and uses it to teach core concepts:
- LangChain tools and agent basics
- Composing agents from tools
- Sub-agents (an agent as a tool)
- RAG with Pinecone + OpenAI embeddings
- Web UI for agent interaction

By the end, you’ll know how to extend Puzzle Agent with your own tools and agents.

---

## 1) Project Tour

Key directories and files:

```
puzzle-agent/
├── main.py                  # CLI orchestrator (REPL)
├── app.py                   # Flask web app (chat UI)
├── templates/index.html     # Web UI (chat, confetti)
├── tools/
│   ├── rag/rag_tool.py      # Pinecone ingestion (RAG)
│   ├── answer_tool.py       # Web search (Tavily)
│   ├── csv_reader.py        # CSV question fetch by row,col
│   ├── length_string.py     # String length tool
│   ├── birthday_tool.py     # Birthday day-of-month tool
│   └── slack_tool.py        # Slack messages
└── agents/
    ├── first_agent.py       # Agent 1 (length + birthday → CSV question)
    └── second_agent.py      # Agent 2 (question/row,col → answer via Tavily → Slack)
```

### Flow

- The puzzle uses two sub-questions to compute indices:
  1. Compute the length of a provided text (row).
  2. Extract the numeric day-of-month from a birthday (col).
- Use `(row, col)` to fetch a question from `data/questionList.csv`.
- Search for the answer with Tavily.
- Post the final answer to Slack.

---

## 2) LangChain Tools

A LangChain tool is a function (often decorated with `@tool`) that returns user-facing text.

Example: `tools/length_string.py`
```python
from langchain_core.tools import tool

@tool
def length_of_string_tool_func(text: str) -> int:
    return len(text)
```

Design tips:
- Tools should be deterministic and concise.
- Keep side effects explicit in return text.

---

## 3) Building Agents

Agents choose which tools to call. We configure each agent with a system prompt, a tool list, and an LLM.

```python
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
```

The first agent computes string length + birthday day-of-month, then fetches the CSV question. The second agent answers (via Tavily) and posts to Slack.

---

## 4) Sub-Agents (Agent-as-a-Tool)

You can wrap Agent 2 as a Tool and let Agent 1 call it directly. This encapsulates RAG+Slack behavior behind a single tool, keeping Agent 1 simple and extensible.

---

## 5) RAG / Bible Search (Vector Retrieval)

`tools/rag/rag_tool.py` ingests `data/bible_bresheit.txt` into Pinecone using OpenAI embeddings. Run ingestion once at startup.

Key notes:
- Embeddings: `OpenAIEmbeddings`
- Vector store: `PineconeVectorStore`
- Env: `OPENAI_API_KEY`, `PINECONE_API_KEY`, `INDEX_NAME`
- Create your index and API key here: [Pinecone](https://www.pinecone.io/)

---

## 6) Web Search (Tavily)

`tools/answer_tool.py` queries Tavily with `include_generated_answer=True` and returns the answer text.

- Sign up / dashboard: [Tavily](https://app.tavily.com/home)
- Env: `TAVILY_API_KEY`

---

## 7) Slack Integration

`tools/slack_tool.py` posts messages to Slack using `SLACK_BOT_TOKEN`. In this workshop, we’ll provide the token so you can send messages to `#rest-ai-workshop`.

---

## 8) Web UI

Run `python app.py`, then open `http://localhost:5000`. The chat page shows both agents’ outputs and triggers confetti on final answers.

---

## 9) Setup & Run

1) Install deps
```bash
pipenv install
```

2) Create `.env` and set:
```bash
OPENAI_API_KEY=...
TAVILY_API_KEY=...
PINECONE_API_KEY=...
INDEX_NAME=...
SLACK_BOT_TOKEN=...
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=...
```

3) Start REPL (CLI)
```bash
python main.py
```

4) Start Web UI
```bash
python app.py
```

Try:
```
Hey puzzle agent, please solve this end-to-end:
1) Calculate the length of 'Hello AI'.
2) Get the numeric day-of-month David Ben Gurion was born.
3) Use row=<length> and column=<day> to fetch the question from the CSV.
4) Answer the question using the Bible data (via Tavily).
5) Send the final answer to the Slack channel.
```

---

## 10) CSV Question Lookup (row, col)

The project reads questions from `data/questionList.csv` using the `CSVReader` tool in `tools/csv_reader.py`.

- **Input format**: a single string `"row,col"` (e.g., `"8,16"`).
- **Indexing**: both row and column are zero-based.
  - **Row 0** is the first data row; **Column 0** is the first column.
  - If you prefer 1-based indices, subtract 1 before calling the tool.
- **Behavior**:
  - Returns the cell at the given row and column.
  - Returns `"Column index out of range"` if the column is beyond that row's length.
  - Returns `"Row not found or empty"` if the row doesn't exist or is empty.
- **Data source**: `data/questionList.csv`.

Example (direct call):

```python
from tools.csv_reader import get_question_from_csv

# Fetch the question at row=8, col=16 (zero-based)
question = get_question_from_csv("8,16")
print(question)
```

In the end-to-end flow, the first agent computes:
- **row**: the length of the provided string
- **col**: the numeric day-of-month from the birthday tool

It then fetches the CSV question at `(row, col)` and passes it to the second agent to answer.

---

## 11) Further Reading

- LangChain docs: https://python.langchain.com/
- Tavily search: [https://app.tavily.com/home](https://app.tavily.com/home)
- Pinecone vectors: https://docs.pinecone.io/
- LangSmith: https://smith.langchain.com/

Happy hacking! 🚀
