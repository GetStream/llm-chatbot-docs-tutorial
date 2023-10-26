import os
import markdown
import itertools
from glob import iglob

# Web app
import streamlit as st
from dotenv import load_dotenv

# File scraping
from bs4 import BeautifulSoup

# Langchain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# HTML
from htmlTemplates import css, bot_template, user_template

from enum import Enum


class SDK(Enum):
    Android = "Android"
    Angular = "Angular"
    Flutter = "Flutter"
    iOS = "iOS"
    React = "React"
    ReactNative = "reactnative"


def handle_question(question):
    response = st.session_state.conversation_bot({"question": question})
    st.session_state.chat_history = response["chat_history"]
    print("Chat history:", st.session_state.chat_history)
    print("Response:", response)
    for i, message in enumerate(reversed(st.session_state.chat_history)):
        if message.type == "ai":
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )
        else:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )


def create_conversation_bot(vector_store):
    print("Creating conversation bot")
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_bot = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    return conversation_bot


def put_data_into_db(text_chunks):
    # TODO: use HF embeddings for free
    print("Putting data into DB")
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def load_text_from_docs(sdk):
    rootdir = f"./data/{sdk.value}/**/*"
    print("Searching for files in", rootdir)
    file_types = ["md", "mdx"]
    ignore_file_types = ["DS_Store", "json", "png", "jpg", "svg", "ico", "jpeg", "gif"]
    files = [f for f in iglob(rootdir, recursive=True) if os.path.isfile(f)]
    filtered_files = list(filter(lambda x: x.split(".")[-1] in file_types, files))
    print(f"Found {len(filtered_files)} relevant files.")

    text_elements = []
    for file in filtered_files:
        print("Processing file:", file)
        with open(file, "r") as f:
            html = markdown.markdown(f.read())
            elements = list(BeautifulSoup(html, "html.parser").find_all())
            headlines = ["h1", "h2", "h3", "h4", "h5"]
            lists = [
                list(group)
                for k, group in itertools.groupby(
                    elements, lambda x: x.name in headlines
                )
                if not k
            ]
            # TODOS:
            # - Lists are doubled
            # - Headlines are omitted - should be part of the text
            # - Some elements are still showing up (e.g. :::note)
            for x in lists:
                text_elements.append(" ".join([el.get_text() for el in x]))

        break
    return text_elements


def main():
    load_dotenv()
    print("Main is executed")

    # setup streamlit app
    st.set_page_config(page_title="Chat with Stream docs", page_icon=":boat:")
    st.write(css, unsafe_allow_html=True)
    st.header("Chat with Stream docs :boat:")

    if "conversation_bot" not in st.session_state:
        print("Conversation bot not found")
        with st.spinner("Loading data..."):
            # load docs data into texts
            texts = load_text_from_docs(SDK.iOS)
            print(f"Found {len(texts)} chunks of texts.")

            # load embeddings
            vector_store = put_data_into_db(texts)

            # create conversation bot
            conversation_bot = create_conversation_bot(vector_store)
            st.session_state.conversation_bot = conversation_bot

    # Add chat history to session state if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    question = st.text_input("Ask a question to our documentation:")
    if question:
        with st.spinner("Thinking..."):
            handle_question(question)


if __name__ == "__main__":
    main()
