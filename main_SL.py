import streamlit as st
import os
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

MD_CHROMA_PATH = "data/chroma_md"  # Path for Markdown files
TXT_CHROMA_PATH = "data/chroma_txt"  # Path for text files
HTML_CHROMA_PATH = "data/chroma_html"  # Path for HTML files

PROMPT_TEMPLATE = """
You are a computer programming tutor. Answer the question based on the following context:

{context}

Don't reference the context in your response, because your student might not have access to it.
---

Answer the question based on the above context: {question}

If the question isn't related to tech, programming, computers, or software, answer the question but also ask the student if they have any computer programming questions. If the student is on-topic, just answer the question.
"""

def main():
    st.sidebar.title("Authentication")
    option = st.sidebar.selectbox("Select Authentication Method", ["API Key", "Gretchen's Password"])

    if option == "API Key":
        api_key = st.sidebar.text_input("Enter Your API Key")
        os.environ["OPENAI_API_KEY"] = api_key
    elif option == "Gretchen's Password":
        password = st.sidebar.text_input("Enter Gretchen's Password", type="password")
        if password == "supersecret":
            # Set Gretchen's API key using environment variable
            os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
        else:
            st.error("Incorrect Password. Access Denied.")
            st.stop()

    # Prepare the DB for Markdown files.
    embedding_function = OpenAIEmbeddings()
    md_db = Chroma(persist_directory=MD_CHROMA_PATH, embedding_function=embedding_function)

    # Prepare the DB for text files.
    txt_db = Chroma(persist_directory=TXT_CHROMA_PATH, embedding_function=embedding_function)

    # Prepare the DB for HTML files.
    html_db = Chroma(persist_directory=HTML_CHROMA_PATH, embedding_function=embedding_function)

    # Initialize ChatOpenAI model.
    model = ChatOpenAI()

    st.title("AI Programming Tutor")

    # Ask user for the question.
    query_text = st.text_input("Enter your question:")

    if not query_text:
        st.warning("Please enter a question.")
        st.stop()

    # Check if the user wants to end the conversation.
    if query_text.lower() == "bye":
        st.write("Computer: Goodbye!")
        st.stop()

    # Search the DB for Markdown files.
    md_results = md_db.similarity_search_with_relevance_scores(query_text, k=3)
    txt_results = txt_db.similarity_search_with_relevance_scores(query_text, k=3)
    html_results = html_db.similarity_search_with_relevance_scores(query_text, k=3)

    # Combine results from all databases
    results = md_results + txt_results + html_results

    if not results:
        st.write("Computer: Unable to find matching results.")
        st.stop()

    results = [(doc, score) for doc, score in results if score >= 0.8]

    if not results:
        context_text = "\n\n---\n\n There is no context. Use your own knowledge."
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Generate prompt.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Invoke OpenAI model.
    response = model.invoke(prompt)

    # Extract response text from the response object
    response_text = response.content.strip(' "')

    # Display the metadata and response text for each result
    if results:
        st.subheader("Matching Results:")
        for doc, score in results:
            st.write(f"Document: {doc.metadata}")
            st.write(f"Relevance Score: {score}")
            st.write("Content:")
            st.write(doc.page_content)
            st.write("-" * 20)

    st.subheader("AI Tutor's Response:")
    st.write(f"AI Tutor: {response_text}")

if __name__ == "__main__":
    main()
