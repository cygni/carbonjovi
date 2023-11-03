# Green Software @ Cygni
This project contains parts of the Cygni Digital Sustainability package that was offered after CTS 2023.

The main components are:
- data-indexer: Python app that scrapes a set of websites and adds the to a ChromaDB for use with ChatGPT
- chat-bot: A Slack-bot that communicates with ChatGPT using the embeddings created by the data-indexer


## Usage:
Everything is based on `npm` and `pipenv` (i.d `Pipfile`).

Invoking `npm`-commands from the root folder should be sufficient.

See below for some common targets. Otherwise why don't you check out the `package.json`-file

```zsh
# runs the website scraper
npm run data-indexer:scrape

# populates the vector database and creates the embeddings based on the scraped websites
npm run data-indexer:embed 

# Compiles the TypeScript code in the Chat-Bot
npm run chat-bot:compile 

# Cleans everything
npm run clean
```