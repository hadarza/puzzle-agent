from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate

from tools.answer_tool import answer_from_csv_tool
from tools.csv_reader import csv_reader_tool
from langchain_openai import ChatOpenAI

from tools.slack_tool import slack_tool


def create_second_agent():
    """Create the second agent for CSV question retrieval and answer generation by searching the answer."""

    # Define tools for the second agent
    tools = [csv_reader_tool, answer_from_csv_tool, slack_tool]

    system_prompt = (
        "You are the second agent. Given either '<row>,<column>' or a question:\n"
        "1) If input looks like '<row>,<column>', call CSVReader to fetch the question.\n"
        "2) Call AnswerFromCSVTool with the question to get an answer.\n"
        "3) Send the answer to Slack via SlackTool.\n"
        "Work autonomously and output the final answer."
    )

    # Build a chat prompt (required by create_tool_calling_agent)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    # Create the LLM for the second agent
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    # Build the tool-calling agent and executor
    agent = create_tool_calling_agent(llm, tools, prompt)

    return agent