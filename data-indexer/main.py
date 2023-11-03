import time
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI

from langchain.chains import LLMChain
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

load_dotenv()
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

condense_question_prompt = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

condense_question_prompt = PromptTemplate.from_template(condense_question_prompt)

condense_question_chain = LLMChain(
    llm=llm,
    prompt=condense_question_prompt,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa_chain = create_qa_with_sources_chain(llm)

doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)


db = Chroma(
    persist_directory="./chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
)

retrieval_qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain,
    retriever=db.as_retriever(),
    memory=memory,
    combine_docs_chain=final_qa_chain,
)

# def predict(message, history):
#     response = retrieval_qa.run({"question": message})
#     responseDict = json.loads(response)
#     answer = responseDict["answer"]
#     sources = responseDict["sources"]

#     if type(sources) == list:
#         sources = "\n".join(sources)

#     if sources:
#         return answer + "\n\nSee more:\n" + sources
#     return answer

# gradio.ChatInterface(predict).launch()

start_time = time.time()
print("Invoking ChatGPT API")

initial_prompt = "You are an intelligent assistant helping Cygni and Accenture employees with their questions regarding green software, digital sustainabilty, environment impact, sustainable solutions etc. " + \
    "Use 'you' to refer to the individual asking the questions even if they ask with 'I' or 'we' or 'my'. " + \
    "The individuals asking the questions are software developers." + \
    "Only use information from the provided sources." + \
    "For tabular information return it as an html table. Do not return markdown format. "

response = retrieval_qa.run({"question": initial_prompt + "What are the Green Software Principles?"})
end_time1 = time.time()
print(response)

# Calculate elapsed time
elapsed_time = (end_time1- start_time) * 1000  # time in milliseconds
print(f"Elapsed time 1: {elapsed_time} ms")

response = retrieval_qa.run({"question": initial_prompt + "What is Cygni?"})
end_time2 = time.time()
print(response)

# Calculate elapsed time
elapsed_time = (end_time2 - end_time1) * 1000  # time in milliseconds
print(f"Elapsed time 2: {elapsed_time} ms")


response = retrieval_qa.run({"question": initial_prompt + "What is Cygni?"})
end_time3 = time.time()
print(response)

# Calculate elapsed time
elapsed_time = (end_time3 - end_time2) * 1000  # time in milliseconds
print(f"Elapsed time 3: {elapsed_time} ms")

# output:
# """
# {
#   "answer": "LangChain provides a standard interface for LLMs, which are language models that take a string as input and return a string as output. To use LangChain with LLMs, you need to understand the different types of language models and how to work with them. You can configure the LLM and/or the prompt used in LangChain applications to customize the output. Additionally, LangChain provides prompt management, prompt optimization, and common utilities for working with LLMs. By combining LLMs with other modules in LangChain, such as chains and agents, you can create more complex applications.",
#   "sources": [
#     "https://python.langchain.com/docs/get_started/quickstart", "https://python.langchain.com/docs/modules/data_connection/document_loaders/markdown"
#   ]
# }
# """