import json
from langchain_core.tools import Tool
from langchain_tavily import TavilySearch

def search_answer_from_csv(query: str) -> str:
    """
    Search for an answer using RAG operations. This function answers a question
    """

    print("Query (Question):")
    print(query)

    tool = TavilySearch(k=1, include_generated_answer=True)
    res = tool.invoke({'query': query})

    print(json.dumps(res, indent=2))

    answer_text = res.get('answer', 'No answer found.')
    return str(answer_text)

answer_from_csv_tool = Tool(
    name="AnswerFromCSVTool",
    func=search_answer_from_csv,
    description="Search for an answer based on the RAG operations and CSV input."
)
