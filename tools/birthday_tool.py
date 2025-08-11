import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from utils.openai_config import llm

load_dotenv()

def get_birthday(person: str = "David Ben Gurion") -> int:
    """Return the numeric day of month for the given person's birthday.

    Uses the centralized LLM and validates the response is a pure integer.
    """
    template = (
        "When was {person} born? Return ONLY the numeric day-of-month as digits, "
        "with no words, punctuation, or explanation. Examples: 'David Ben-Gurion' -> 16. "
        "Output must be a single integer like: 16"
    )
    prompt_template = PromptTemplate(template=template, input_variables=["person"])

    formatted_prompt = prompt_template.format(person=person)
    prompt_message = HumanMessage(content=formatted_prompt)
    response = llm.invoke([prompt_message])
    response_content = (getattr(response, "content", "") or "").strip()

    # Validate and return integer day with regex fallback
    import re
    text = response_content.strip()
    if text.isdigit():
        day = int(text)
    else:
        m = re.search(r"\b(\d{1,2})\b", text)
        if not m:
            raise ValueError(
                f"Could not extract numeric day from response: {response_content}"
            )
        day = int(m.group(1))

    if not (1 <= day <= 31):
        raise ValueError(f"Extracted day out of range: {day}")
    return day


birthday_tool = Tool(
    name="BirthdayTool",
    func=get_birthday,
    description="Returns the numeric birth day-of-month for a person"
)