import os
import asyncio
import aiohttp
import json
import re

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_sdk.socket_mode.aiohttp import SocketModeClient
#from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv
load_dotenv()

import ai

# Setup the slack stuff

# Initializes your app with your bot token and socket mode handler
app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

bullet = "•"

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
@app.message("help")
async def message_help(message, say):
    print(f"Help requested [user={message['user']}]")
    help_text = f"""
:wave: <@{message['user']}>, I got your back :green_heart:
Simply ask me anything about <https://greensoftware.cygni.se|Green Software> as a direct *message* and I will try to answer!

Some examples:
{bullet} What is Green Software?
{bullet} What patterns should I consider when setting up a new Kubernetes cluster?
{bullet} Are you Bon Jovi?

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

def format_response(response):
    urls = response['sources']

    # Filter the list to exclude any URL containing the word "hello"
    filtered_urls = [url for url in urls if "carbonjovi-docs" not in url]

    if len(filtered_urls) <= 0:
        answer = response['answer']
    elif contains_url(response['answer']):
        answer = response['answer']
    else:
        delim = "\n"
        sources = delim.join(bullet + " " + item for item in filtered_urls)
        answer = f"""{response['answer']}

Sources:
{sources}
"""
    return answer.replace("**", "*")

@app.event("app_mention")
async def handle_app_mention_events(body, client, event):
    print('event.app_mention')


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

async def remove_reaction(event, client, reaction):
    # Adding a reaction to the message asynchronously
    try:
        await client.reactions_remove(
            channel=event['channel'],
            timestamp=event['ts'],
            name=reaction
        )
    except Exception as e:
        print(f"Error removing reaction: {e}")


@app.event("message")
async def handle_message_events(event, say, context, client):
    print(f"event.message [user={event['user']}, text={event['text']}]")

    # Status indicator – message received
    await add_reaction(event, client, "popcorn")

    # Query the model
    response = await ai.query_ai(event['text'], event['user'])

    # Query completed
    await add_reaction(event, client, "white_check_mark")

    answer = format_response(json.loads(response))

    print("Event: ")
    print(event)

    response_message = {"text": ":seedling:\n" + answer, "unfurl_links": False, "unfurl_media": False}
    if "thread_ts" in event:
        response_message['thread_ts'] = event["thread_ts"]

    # Send the answer
    await say(response_message)

    # Status indicator – message received
    await remove_reaction(event, client, "popcorn")

async def async_main():
    print("Starting @CarbonJovi")
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()

# Start the Bot
if __name__ == "__main__":
    asyncio.run(async_main())
