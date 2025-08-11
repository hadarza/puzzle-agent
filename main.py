import os
from dotenv import load_dotenv
from agents.first_agent import create_first_agent
from agents.second_agent import create_second_agent
from tools.rag.rag_tool import ingest_bible

# Load environment variables
load_dotenv()

def main():
    """Main function to run the agents"""
    print("🚀 Starting Puzzle Agent...")

    print("\n✅ First agent:")
    print("\nAvailable capabilities:")
    print("• String length calculation")
    print("• Birthday retrieval")
    print("\n" + "=" * 50)

    ingest_bible("data/bible_bresheit.txt")

    print("\n✅ Second agent:")
    print("\nAvailable capabilities:")
    print("• RAG search and answer generation")
    print("• Slack integration")
    print("\n" + "=" * 50)

    # Create agents once
    agent_executor_1 = create_first_agent()
    create_second_agent()

    while True:
        try:
            user_input = input("\n🤖 Ask me anything (or 'quit' to exit): ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not user_input:
                continue

            print(f"\n🔍 Processing: {user_input}")
            print("-" * 30)

            # Run first agent; it should compute row/column and fetch QUESTION
            result_1 = agent_executor_1.invoke({"input": user_input})
            output_text = (result_1.get("output") or "").strip()
            print(output_text)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    main()


