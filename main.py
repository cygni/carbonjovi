import os
import json
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv
load_dotenv()

import ai

# Setup the slack stuff

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

bullet = "•"

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
@app.message("help")
def message_help(message, say):
    print(f"Help requested [user={message['user']}]")
    help_text = f"""
:wave: <@{message['user']}>, I got your back :green_heart:
Simply ask me anything about <https://greensoftware.cygni.se|Green Software> as a direct *message* and I will try to answer!

Some examples:
{bullet} What is Green Software?
{bullet} What patterns should I consider when setting up a new Kubernetes cluster?

There are a few special quirks, you can also ask for:
{bullet} `help` shows this text
"""
    # Send the help message to the caller
    say({"type": "mrkdwn", "text": help_text, "unfurl_links": False, "unfurl_media": False})

#     say({"text": help_text, "type":"mrkdwn", "unfurl_links": False, "unfurl_media": False})

#     {
#   "type": "section",
#   "text": {
#     "type": "mrkdwn",
#     "text": "New Paid Time Off request from <example.com|Fred Enriquez>\n\n<https://example.com|View request>"
#   }
# }

@app.event("reaction_added")
def handle_message_events(body, client, event, context):
    print(type(client))
    print(type(event))
    print(type(body))
    result = client.chat_postMessage(channel=context.channel_id, text="thanks!")
    print("message posted")
    print(type(result))


def contains_url(string):
    # Regular expression to match URLs
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^()\s<>]+|\(([^()\s<>]+|(\([^()\s<>]+\)))*\))+(?:\(([^()\s<>]+|(\([^()\s<>]+\)))*\)|[^`!()\[\]{};:'\".,<>?«»“”‘’]))"

    # Check if the string contains any URLs
    return bool(re.search(url_pattern, string))

def format_response(response):
    if len(response['sources']) <= 0:
        answer = response['answer']
    elif contains_url(response['answer']):
        answer = response['answer']
    else:
        delim = "\n"
        sources = delim.join(bullet + " " + item for item in response['sources'])
        answer = f"""{response['answer']}

Sources:
{sources}
"""
    return answer.replace("**", "*")

@app.event("app_mention")
def handle_app_mention_events(body, client, event):
    print('event.app_mention')


@app.event("message")
def handle_message_events(event, say, context, client):
    print(f"event.message [user={event['user']}, text={event['text']}]")
    print(type(client))

    # Start a simple wait message
    #wait_response = say(':hourglass_flowing_sand:')

    # Query the model
    response = ai.query_ai(event['text'], event['user'])
    answer = format_response(json.loads(response))


    # delete the wait message
    #ts = wait_response["ts"]
    #client.chat_delete(channel=context.channel_id, ts=ts)
    #client.chat_update(channel=context.channel_id, ts=ts, text=":seedling:")

    print("Event: ")
    print(event)

    response_message = {"text": ":seedling:\n" + answer, "unfurl_links": False, "unfurl_media": False}
    if "thread_ts" in event:
        response_message['thread_ts'] = event["thread_ts"]

    # Send the answer as soon as possible
    say(response_message)

# Start the Bot
if __name__ == "__main__":
    print("Starting @CarbonJovi")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
