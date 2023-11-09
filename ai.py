import time

from langchain.chat_models import ChatOpenAI

from langchain.chains import LLMChain
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

print('Setting up chat')
#llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
#llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

condense_question_prompt = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

print('Setting up condense prompt')
condense_question_prompt = PromptTemplate.from_template(condense_question_prompt)

condense_question_chain = LLMChain(
    llm=llm,
    prompt=condense_question_prompt,
)

print('Initializing memory')
memories = {}

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

print('Creating chain')
qa_chain = create_qa_with_sources_chain(llm)

print('Setting up template')
doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

print('Setting up stuff document chain')
final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)

print('Opening vector database')
db = Chroma(
    persist_directory="./chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
)


initial_prompt = """You are an intelligent Slack-bot assistant helping Cygni and Accenture employees with their questions regarding green software, digital sustainabilty, environment impact, sustainable solutions etc. 
You communicate via Slack, therefore you are a Slack-bot. Your bot-name is CarbonJovi, the name implies a mix of 'Carbon' and 'Bon Jovi'. You are humorous and uses Slack emojis.
Use 'you' to refer to the individual asking the questions even if they ask with 'I' or 'we' or 'my'. 
The individuals asking the questions are software developers aspiring to be 'Green Software Practitioners'.
Only use information from the provided sources.
All output should be in Markdown format. Keep every paragraph brief with simple language, the audience are not native English speakers.
"""

print('Setup of AI completed')

retrieval_chains = {}
chains = {}

def get_or_create_retrieval_chain(user_id):
    chain_info = {}
    #chain_info["user_id"] = user_id

    if user_id in chains:
        print(f'Chain already created for user {user_id}')
    else:
        chain_info = {}
        chain_info["user_id"] = user_id
        chain_info["is_new"] = True

        print(f'Creating retrieval chain for user {user_id}')
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        retrieval_qa = ConversationalRetrievalChain(
            question_generator=condense_question_chain,
            retriever=db.as_retriever(),
            memory=memory,
            combine_docs_chain=final_qa_chain,
        )

        chain_info["chain"] = retrieval_qa
        chains[user_id] = chain_info

    return chains[user_id]

def run_query(chain_info, question):
    chain = chain_info.get("chain")

    if chain_info.get("is_new"):
        response = chain.run({"question": initial_prompt + question})
        chain_info["is_new"] = False
    else:
        response = chain.run({"question": initial_prompt + question})

    return response

def query_ai(question, user_id):
    print(f"Querying the AI [userId={user_id}, question={question}]")
    start_time = time.time()

    chain_info = get_or_create_retrieval_chain(user_id)
    response = run_query(chain_info, question)
    end_time = time.time()
    elapsed_time = (end_time- start_time) * 1000  # time in milliseconds
    
    print(f"Elapsed time 1: {elapsed_time} ms")
    print(type(response))
    return response
