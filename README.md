# Puzzle Agent

## Overview
Puzzle Agent is a multi-agent system designed to perform a series of tasks including calculating string lengths, retrieving birthdays, fetching questions from a CSV file, generating answers, and sending messages to a Slack channel. The system is built using LangChain and integrates with various tools to achieve its functionality.

## Features
- **String Length Calculation:** Calculate the length of a given string.
- **Birthday Retrieval:** Retrieve the day of the month for a given person's birthday.
- **CSV Reading:** Use calculated indices to fetch a question from a CSV file.
- **Answer Generation:** Generate an answer based on the fetched question.
- **Slack Integration:** Send messages to a specified Slack channel.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd puzzle-agent
   ```

2. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pipenv install
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory and add the following (we’ll provide some of them):
   ```
   # OpenAI
   OPENAI_API_KEY=<your-openai-api-key>

   # Tavily Search (sign up to get an API key)
   # Dashboard: https://app.tavily.com/home
   TAVILY_API_KEY=<your-tavily-api-key>

   # Pinecone (vector DB for RAG)
   # Console: https://www.pinecone.io/  → create an index and API key
   PINECONE_API_KEY=<your-pinecone-api-key>
   INDEX_NAME=<your-index-name>

   # Slack bot token (we will provide this; used to send to #rest-ai-workshop)
   SLACK_BOT_TOKEN=<your-slack-bot-token>

   # LangSmith tracing
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=https://api.smith.langchain.com
   LANGSMITH_API_KEY=<your-langsmith-api-key>
   ```

4. **Run the Application:**
   ```bash
   python3 main.py
   ```

You can run
```bash
python3 app.py
``` if you want to see the result in UI.

5. The input should be pasted from below:
```
Hey Puzzle Agent, please solve this puzzle end to end:

1. Calculate the length of "Hello AI".
2. Find the numeric day of the month on which David Ben-Gurion was born.
3. Use these values as the row (length) and column (birthday) to fetch the question from the CSV.
4. Answer the question using the Bible data (via Tavily).
5. Send the final answer to the designated Slack channel.

```

## Usage
- **Interactive Mode:**
  - Start the application and interact with the agents by providing inputs such as strings for length calculation or names for birthday retrieval.
  - The agents will autonomously decide when to use the Slack tool to send messages based on the context of the conversation.


## 🏗️ Project Structure

```
puzzle-agent/
├── agents/
│   ├── first_agent.py           # First agent: length + birthday → CSV question
│   └── second_agent.py          # Second agent: CSV/question → Tavily answer → Slack
├── data/
│   ├── bible_bresheit.txt       # RAG source text
│   └── questionList.csv         # Questions grid (row=length, col=birthday day)
├── tools/
│   ├── answer_tool.py           # Tavily-based answering tool
│   ├── birthday_tool.py         # Returns numeric day-of-month via LLM
│   ├── csv_reader.py            # Returns question from CSV by row,col
│   ├── length_string.py         # Returns length of a string
│   ├── slack_tool.py            # Sends a message to Slack
│   └── rag/
│       └── rag_tool.py          # Pinecone ingestion for RAG
├── utils/
│   └── openai_config.py         # Centralized LLM config
├── templates/
│   └── index.html               # Web UI for chat
├── app.py                       # Flask app for chat UI
├── main.py                      # CLI runner (REPL)
├── README.md
├── Pipfile / Pipfile.lock
└── .env                         # Environment variables (not committed)
```

## 🔧 Tools (detailed)

- LengthOfString (`tools/length_string.py`)
  - Purpose: Return the character length of a string using Python `len()`.
  - Signature: `length_of_string_tool_func(text: str) -> int`
  - Input: Plain text string.
  - Output: Integer (number of characters).
  - Notes: Exposed to agents as `LengthOfString`.

- BirthdayTool (`tools/birthday_tool.py`)
  - Purpose: Return the numeric day-of-month for a person's birthday via LLM.
  - Signature: `get_birthday(person: str = "David Ben Gurion") -> int`
  - Input: Person's full name (string).
  - Output: Integer in range 1–31.
  - Robustness: Enforces digits-only in prompt and applies regex fallback (extracts 1–2 digit number from responses like “born on the 16th”). Validates range.
  - Env: Uses `OPENAI_API_KEY` via `utils/openai_config.py`.
  - Exposed as `BirthdayTool`.

- CSVReader (`tools/csv_reader.py`)
  - Purpose: Fetch a question from a CSV, indexed by row and column.
  - Signature: `get_question_from_csv(row_col: str) -> str`
  - Input: String in the form `"<row>,<col>"` (both zero-based integers).
  - Output: Question text (string) or friendly error message if out of range.
  - Data: Reads `data/questionList.csv`.
  - Exposed as `CSVReader`.

- AnswerFromCSVTool (`tools/answer_tool.py`)
  - Purpose: Generate an answer to a question using Tavily search (RAG-lite).
  - Signature: `search_answer_from_csv(query: str) -> str`
  - Input: The question string.
  - Output: Answer text from Tavily (`include_generated_answer=True`).
  - Env: `TAVILY_API_KEY`. Sign up and manage your key in the Tavily dashboard: [Tavily](https://app.tavily.com/home)
  - Exposed as `AnswerFromCSVTool`.

- SlackTool (`tools/slack_tool.py`)
  - Purpose: Send a message to a Slack channel.
  - Signature: `send_to_slack_channel(message: str) -> None`
  - Input: Message text (string).
  - Output: None (posts to Slack; prints status/errors).
  - Env: `SLACK_BOT_TOKEN`, channel ID configured in the module.
  - Exposed as `SlackTool`.

- RAG Ingestion (`tools/rag/rag_tool.py`)
  - Purpose: Ingest and index `data/bible_bresheit.txt` into Pinecone for retrieval.
  - Signature: `ingest_bible(file_path: str) -> PineconeVectorStore`
  - Input: Path to text file.
  - Output: Pinecone vector store handle (returned). Side-effect: populates index.
  - Env: `OPENAI_API_KEY` (embeddings), `PINECONE_API_KEY`, `INDEX_NAME`. Create your index and get your API key in the Pinecone console: [Pinecone](https://www.pinecone.io/)
  - Usage: Run once at startup (not an agent tool by default).

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.
