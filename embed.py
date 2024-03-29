import json

from langchain_community.document_loaders import (
    BSHTMLLoader,
    DirectoryLoader,
)

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

loader = DirectoryLoader(
        "./scrape",
        glob="*.html",
        loader_cls=BSHTMLLoader,
        show_progress=True,
        loader_kwargs={"get_text_separator": " "},
)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
)
documents = text_splitter.split_documents(data)

# map sources from file directory to web source
with open("./scrape/sitemap.json", "r") as f:
        sitemap = json.loads(f.read())

for document in documents:
        document.metadata["source"] = sitemap[
                document.metadata["source"].replace(".html", "").replace("scrape/", "")
        ]

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
#embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
db = Chroma.from_documents(
    documents, 
    embedding_model,
    persist_directory="./chroma"
)
db.persist()
