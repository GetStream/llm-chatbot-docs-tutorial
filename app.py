import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import itertools
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


def ask_question(question, conversation_bot):
    response = conversation_bot({"question": question})
    return response


def create_conversation_bot(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_bot = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    return conversation_bot


def put_data_into_db(text_chunks):
    # TODO: use HF embeddings for free
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def load_text_from_docs():
    with open("./data/iOS/client/offline-support.md", "r") as f:
        html = markdown.markdown(f.read())
        elements = list(BeautifulSoup(html, "html.parser").find_all())
        headlines = ["h1", "h2", "h3", "h4", "h5"]
        lists = [
            list(group)
            for k, group in itertools.groupby(elements, lambda x: x.name in headlines)
            if not k
        ]
        # TODOS:
        # - Lists are doubled
        # - Headlines are omitted - should be part of the text
        # - Some elements are still showing up (e.g. :::note)
        text_elements = []
        for x in lists:
            text_elements.append(" ".join([el.get_text() for el in x]))

        # print(len(text_elements))
        # print("--------------------------")
    return text_elements


def main():
    load_dotenv()

    # load docs data into texts
    texts = load_text_from_docs()
    print(f"Found {len(texts)} chunks of texts.")

    # load embeddings
    vector_store = put_data_into_db(texts)

    # create conversation bot
    conversation_bot = create_conversation_bot(vector_store)

    # ask question
    response = ask_question("How does connection recovery work?", conversation_bot)

    print(response)


if __name__ == "__main__":
    main()
