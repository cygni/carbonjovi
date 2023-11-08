import dotenv from 'dotenv';

dotenv.config();

import { ChatOpenAI } from "langchain/chat_models/openai"
import { LLMChain } from "langchain/chains";

import { PromptTemplate } from 'langchain/prompts';







import { RetrievalQAChain } from "langchain/chains";



import { Chroma } from "langchain/vectorstores/chroma";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { TextLoader } from "langchain/document_loaders/fs/text";



async function start(): Promise<string> {

    // Create docs with a loader
    // const loader = new TextLoader("src/document_loaders/example_data/example.txt");
    // const docs = await loader.load();

    const vectorStore = await Chroma.fromExistingCollection(
        new OpenAIEmbeddings({ modelName: "text-embedding-ada-002" }),
        { url: "file:///Users/tommy.wassgren/EDF/greensoftware/data-indexer/chroma2" }
    );

    const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo", openAIApiKey: process.env.OPENAI_API_KEY });
    const chain = RetrievalQAChain.fromLLM(model, vectorStore.asRetriever());




    /*




        dbConfig
        ["Hello world", "Bye bye", "hello nice world"],
        [{ id: 2 }, { id: 1 }, { id: 3 }],
        new OpenAIEmbeddings()*/


    return "";
};

start().then(r => console.log('Result ' + r));



// new Chroma(empeddings)
// // Create vector store and index the docs
// const vectorStore = await Chroma.fromExistingCollection(fromDocuments(docs, new OpenAIEmbeddings(), {
//     collectionName: "a-test-collection",
//     url: "http://localhost:8000", // Optional, will default to this value
//     collectionMetadata: {
//         "hnsw:space": "cosine",
//     }, // Optional, can be used to specify the distance method of the embedding space https://docs.trychroma.com/usage-guide#changing-the-distance-function
// });



// const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo", openAIApiKey: process.env.OPENAI_API_KEY });
// const chain = RetrievalQAChain.fromLLM(model, vectorStore.asRetriever());

/*
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.memory import ConversationBufferMemory

# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.prompts import PromptTemplate
# from langchain.vectorstores import Chroma

*/
console.log('Hello world');
console.log('API KEY=' + process.env.OPENAI_API_KEY);
