import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from langchain_core.tools import Tool

# Set up Slack client
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Define the Slack tool function
def send_to_slack_channel(message: str) -> None:
    """Send a message to a dadicate slack channel"""
    try:
        print(f"Sending message to Slack channel: {message}")
        response = slack_client.chat_postMessage(
            channel="C099ZL7L9EG",
            text=message
        )
        print(f"Message sent to Slack channel: {response['channel']}")
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")

# Define the Slack tool
slack_tool = Tool(
    name="SlackTool",
    func=send_to_slack_channel,
    description="Sends a message to a specified Slack channel."
)
