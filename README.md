# @CarbonJovi
`@CarbonJovi` is a Slack-bot that can answer questions about Green Software.


* The data is fetched from various sources and stored in a Vector database.
* The Vector database is commited with the project and deployed on disk
* The Slack-bot is written in Python using Bolt and uses the on-disk Vector database

This indexer is heavily influenced by this article: https://jasonwebster.dev/blog/chatting-to-a-website-with-langchain-openai-and-chromadb

## Pipenv
`pipenv` is used for the Python parts.

Check the `Pipfile` for specific Python version requirements.

* `pipenv shell` – starts/creates a virtual environment
* `pipenv install` – installs all required packages specified in the Pipfile
