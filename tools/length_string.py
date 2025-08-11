from langchain_core.tools import Tool
from langchain.prompts.prompt import PromptTemplate

length_prompt = PromptTemplate(
    template="""Count the number of characters in the following string.
    Return only the numeric count, without any explanation or additional text:
    {input_string}""",
    input_variables=["input_string"],
)

def length_of_string_tool_func(text: str) -> int:
    length = len(text)

    # Define ANSI escape codes for color
    GREEN = '\033[92m'
    RESET = '\033[0m'

    # Print the response content with color
    print(f"{GREEN}✅ Length of string: {length}{RESET}")
    
    return length

length_of_string_tool = Tool(
    name="LengthOfString",
    func=length_of_string_tool_func,
    description="Returns the length of the input string (number of characters)."
)