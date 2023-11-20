import os
import asyncio
import json
import re

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler

from dotenv import load_dotenv
load_dotenv()

import ai

# Setup the slack stuff

# Initializes your app with your bot token and socket mode handler
app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

bullet = "•"

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
async def message_help(event, say):
    print(f"Help requested [user={event['user']}]")
    help_text = f"""
:wave: <@{event['user']}>, I got your back :green_heart:
Simply ask me anything about <https://greensoftware.cygni.se|Green Software> as a direct *message* and I will try to answer!

Some examples:
{bullet} What is Green Software?
{bullet} What patterns should I consider when setting up a new Kubernetes cluster?
{bullet} Are you Bon Jovi?

Note that there is a limit on the number of tokens you can use, and conversations will sometimes be reset due to usage or server restarts.

There are a few special quirks, you can also ask for:
{bullet} `help` shows this text
"""
    # Send the help message to the caller
    await say({"type": "mrkdwn", "text": help_text, "unfurl_links": False, "unfurl_media": False})

def contains_url(string):
    # Regular expression to match URLs
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^()\s<>]+|\(([^()\s<>]+|(\([^()\s<>]+\)))*\))+(?:\(([^()\s<>]+|(\([^()\s<>]+\)))*\)|[^`!()\[\]{};:'\".,<>?«»“”‘’]))"

    # Check if the string contains any URLs
    return bool(re.search(url_pattern, string))

def filter_urls_in_respomse(response):
    filtered_urls = response['sources']
    filtered_urls = [url for url in filtered_urls if "carbonjovi-docs" not in url]
    filtered_urls = [url for url in filtered_urls if "cygni.se" not in url]
    filtered_urls = [url for url in filtered_urls if "accenture.com" not in url]
    filtered_urls = [url for url in filtered_urls if "bonjovi" not in url]
    filtered_urls = [url for url in filtered_urls if "bon-jovi" not in url]
    filtered_urls = [url for url in filtered_urls if "Bon_Jovi" not in url]
    return filtered_urls

def format_response(response):
    # Get answer, do some replacements
    answer = response['answer'].replace("**", "*")

    # Blocks are needed for Slack formatting
    blocks = [
        {
            "type" : "section",
            "text" : {"type" : "mrkdwn", "text" : answer } 
        }
    ]

    # Filter the list to exclude any URL containing the word "hello"
    filtered_urls = filter_urls_in_respomse(response)
    if (len(filtered_urls) > 0):
        # If there are sources, append them with a divider
        blocks.append({ "type" : "divider" })

        # The actual urls
        urls = []
        for url in filtered_urls:
            urls.append({ 
                "type" : "rich_text_list", 
                "style" : "bullet", 
                "elements": [
                    {
                        "type" : "rich_text_section", 
                        "elements": [ 
                            {
                                "type" : "link", 
                                "url": url
                            }
                        ]
                    }
                ]
            })

        # Formatted as a list
        blocks.append({ "type" : "rich_text", "elements" : urls })

    return { "answer": answer, "blocks" : blocks }

async def add_reaction(event, client, reaction):
    # Adding a reaction to the message asynchronously
    try:
        await client.reactions_add(
            channel=event['channel'],
            timestamp=event['ts'],
            name=reaction
        )
    except Exception as e:
        print(f"Error adding reaction: {e}")

async def async_query_ai(future, query, user_id):
    # Query the model
    response = await ai.query_ai(query, user_id)
    future.set_result(response)

WAIT_SECONDS = 2

TOO_LONG = """:spock-hand: Oops! Your question's a bit too long for me to handle. Could you trim it down a bit? :blush:"""

WAITING_REACTION = "popcorn"
THINKING_REACTION = "brain"
COMPLETED_REACTION = "white_check_mark"

@app.event("message")
async def handle_message_events(event, say, client):
    print(f"handle_message_events [user={event['user']}, text={event['text']}]")

    # Status indicator – message received
    await add_reaction(event, client, WAITING_REACTION)

    user_text = event["text"].strip()

    if (user_text == "help"):
        await add_reaction(event, client, THINKING_REACTION)
        await message_help(event, say)
        await add_reaction(event, client, COMPLETED_REACTION)
        return

    if (len(user_text) > 1024):
        await add_reaction(event, client, THINKING_REACTION)
        await say(TOO_LONG)
        await add_reaction(event, client, COMPLETED_REACTION)
        return

    # Alright, let's pass the message on to the llm
    ai_future = asyncio.Future()
    asyncio.create_task(async_query_ai(ai_future, user_text, event["user"]))
    
    await asyncio.sleep(WAIT_SECONDS)
    await add_reaction(event, client, THINKING_REACTION)

    # Wait for response
    formatted_response = await ai_future

    # Query completed
    await add_reaction(event, client, "white_check_mark")

    formatted_response = format_response(json.loads(formatted_response))

    response_message = {
        "text": formatted_response["answer"], 
        "blocks": formatted_response["blocks"], 
        "unfurl_links": False, 
        "unfurl_media": False
    }

    if "thread_ts" in event:
        response_message['thread_ts'] = event["thread_ts"]

    # Send the answer
    await say(response_message)


async def async_main():
    print("Starting @CarbonJovi")
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

# Start the Bot
if __name__ == "__main__":
    asyncio.run(async_main())
