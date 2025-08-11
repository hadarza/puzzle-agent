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
   Create a `.env` file in the root directory and add the following:
   ```
   OPENAI_API_KEY=<your-openai-api-key>
   TAVILY_API_KEY=<your-tavily-api-key>
   INDEX_NAME=<your-index-name>
   LANGSMITH_TRACING=<your-langsmith-tracing>
   LANGSMITH_ENDPOINT=<your-langsmith-endpoint>
   LANGSMITH_API_KEY=<your-langsmith-api-key>
   PINECONE_API_KEY=<your-pinecone-api-key>
   SLACK_BOT_TOKEN=<your-slack-bot-token>
   SLACK_CHANNEL_ID=<your-slack-channel-id>
   ```

4. **Run the Application:**
   ```bash
   python3 main.py
   ```

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

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.

hadarza@wix.com
