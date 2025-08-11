import csv
import os
from langchain_core.tools import Tool

def read_csv_question(file_path: str, row: int, col: int) -> str:
    """Read a question from a CSV file based on the specified row and column."""
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, line in enumerate(reader):
            if i == row:
                if col < len(line):
                    return line[col]
                else:
                    return "Column index out of range"
    return ""

# Get the absolute path to the CSV file
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/questionList.csv")

def get_question_from_csv(row_col: str) -> str:
    row, col = map(int, row_col.split(","))
    print(f"Reading CSV at row: {row}, column: {col}")
    question = read_csv_question(file_path, row, col)
    if not question:
        return "Row not found or empty"
    return question

csv_reader_tool = Tool(
    name="CSVReader",
    func=get_question_from_csv,
    description="Get question from CSV by row,col"
)
