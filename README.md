# @greensoftware/data-indexer
Scrapes and indexes/vectorizes a dataset from the web. 

This indexer is heavily influenced by this article: https://jasonwebster.dev/blog/chatting-to-a-website-with-langchain-openai-and-chromadb

## NPM vs Pipenv
NPM is used througout the project to invoke all commands but `pipenv` is used for the Python parts. However,
`npm` is used to wrap the `pipenv`-commands so that devs only need to know about one technology for running/compiling etc.