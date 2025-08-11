import logging

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.qa_generation.prompt import templ
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.tools import render_text_description, tool
from langchain_openai import ChatOpenAI

from tools.csv_reader import csv_reader_tool
from tools.length_string import length_of_string_tool
from tools.birthday_tool import birthday_tool
from tools.slack_tool import slack_tool


def create_first_agent(user_input: str | None = None):
    """Create the first agent executor. If user_input is provided, run once and return result; otherwise return the executor."""

    template = "Answer the following questions. Use the given tools: {tools}"

    # Define tools for the first agent
    tools = [length_of_string_tool, birthday_tool, csv_reader_tool, slack_tool]

    human_message = HumanMessagePromptTemplate.from_template(template)
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )
    # Create the LLM for the first agent
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
    )

    # Create the first agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    if user_input is None:
        return executor
    return executor.invoke({"input": user_input})

@tool
def calculate_string_length(text: str) -> int:
    """Calculate the length of a string."""
    length_result = length_of_string_tool.func(text)
    return int(length_result)

@tool
def get_birthday(person_name: str) -> int:
    """Retrieve the birthday of a given person name as a numeric day."""
    print(f"Retrieving the birthday of {person_name}.")
    birthday_result = birthday_tool.func()
    print(f"Birthday result: {birthday_result}")

    return int(birthday_result)