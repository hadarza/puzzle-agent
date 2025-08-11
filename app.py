import re
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from agents.first_agent import create_first_agent
from agents.second_agent import create_second_agent
from tools.rag.rag_tool import ingest_bible


load_dotenv()

app = Flask(__name__)


# Initialize agents and ingest RAG data once at startup
agent_executor_1 = None
agent_executor_2 = None

def initialize_agents_once() -> None:
    global agent_executor_1, agent_executor_2
    if agent_executor_1 is None or agent_executor_2 is None:
        # Ingest RAG data (idempotent if index already exists)
        try:
            ingest_bible("data/bible_bereishit.txt")
        except Exception as e:
            # Do not crash the app if ingestion fails; surface error later when needed
            print(f"Warning: RAG ingestion failed or skipped: {e}")

        # Create executors
        agent_executor_1 = create_first_agent()
        agent_executor_2 = create_second_agent()


def parse_row_col_and_question(output_text: str):
    output_text = (output_text or "").strip()
    row = col = None
    question = None

    m = re.search(r"ROW\s*=\s*(\d+)\s*;\s*COLUMN\s*=\s*(\d+)", output_text, re.IGNORECASE)
    if m:
        row = int(m.group(1))
        col = int(m.group(2))

    q_match = re.search(r"QUESTION:\s*(.+)", output_text, re.IGNORECASE)
    if q_match:
        question = q_match.group(1).strip()

    return row, col, question


@app.route("/")
def index():
    initialize_agents_once()
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    initialize_agents_once()

    # Accept either form or JSON
    user_input = request.form.get("message") or (request.json.get("message") if request.is_json else None)
    if not user_input:
        return jsonify({"error": "Missing 'message'"}), 400

    try:
        # First agent
        result_1 = agent_executor_1.invoke({"input": user_input})
        first_output = (result_1.get("output") or "").strip()
        row, col, question = parse_row_col_and_question(first_output)

        second_input = None
        if question:
            second_input = question
        elif row is not None and col is not None:
            second_input = f"{row},{col}"

        result_2_output = None
        if second_input:
            result_2 = agent_executor_2.invoke({"input": second_input})
            result_2_output = (result_2.get("output") or "").strip()

        return jsonify({
            "first_agent_output": first_output,
            "row": row,
            "column": col,
            "question": question,
            "second_agent_input": second_input,
            "second_agent_output": result_2_output,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


