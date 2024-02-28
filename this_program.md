This script, `create_database.py`, serves to generate a database of text chunks from various types of documents such as HTML, Markdown, and plain text files. It first loads documents from the specified directory using specific file patterns (`*.html`, `*.md`, `*.txt`). Then, it splits the content of each document into smaller text chunks using a text splitter algorithm. After splitting, it saves these chunks to separate directories corresponding to each document type (`chroma_html`, `chroma_md`, `chroma_txt`). Finally, it initializes a database using the `Chroma` vector store, utilizing the `OpenAIEmbeddings` for embeddings, and persists the database to disk. The script also prints out some information about the documents processed and the chunks generated during the process.

# python3 create_database.py

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil

DATA_PATH = "data"
CHROMA_PATH_HTML = os.path.join(DATA_PATH, "chroma_html")
CHROMA_PATH_MD = os.path.join(DATA_PATH, "chroma_md")
CHROMA_PATH_TXT = os.path.join(DATA_PATH, "chroma_txt")


def main():
    generate_data_store()

def generate_data_store():
    # Process HTML files if they exist
    html_documents = load_documents("*.html")
    if html_documents:
        html_chunks = split_text(html_documents)
        save_to_chroma(html_chunks, CHROMA_PATH_HTML, len(html_documents))
    else:
        print("No HTML files found in the directory. Skipping HTML processing.")

    # Process Markdown files
    md_documents = load_documents("*.md")
    if md_documents:
        md_chunks = split_text(md_documents)
        save_to_chroma(md_chunks, CHROMA_PATH_MD, len(md_documents))
    else:
        print("No markdown files found in the directory. Skipping markdown processing.")

    # Process txt files
    txt_documents = load_documents("*.txt")
    if txt_documents:
        txt_chunks = split_text(txt_documents)
        save_to_chroma(txt_chunks, CHROMA_PATH_TXT, len(txt_documents))
    else:
        print("No text files found in the directory. Skipping text processing.")

def load_documents(glob_pattern):
    loader = DirectoryLoader(DATA_PATH, glob=glob_pattern)
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Print an example document and its metadata
    document = chunks[1]
    print(f"Document content: {document.page_content}\n\n\n")
    print(f"Document metadata: {document.metadata}")

    return chunks

def save_to_chroma(chunks: list[Document], chroma_path: str, num_files: int):
    # Clear out the database directory first.
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    # Create a new database from the chunks.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=chroma_path
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {chroma_path}.")
    print(f"Added {num_files} files to the database.")

if __name__ == "__main__":
    main()





This program serves as a computer programming tutor by leveraging OpenAI's GPT-based models to provide answers to programming-related questions. It prompts the user to enter a question, searches a database of programming-related content for similar contexts, and then formulates a response based on the provided context and the input question. The response is generated using OpenAI's ChatGPT model. Additionally, the program prints metadata about the retrieved documents and the relevance scores associated with them, along with the content of each document, to provide additional context for the response. If an API key is not provided, it prompts the user to enter it.


import argparse
import os
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "data/chroma_md"  # Update the path to point to the "chroma_md" directory

PROMPT_TEMPLATE = """
You are a computer programming tutor. Answer the question based on the following context:

{context}

Don't reference the context in your response, because your student might not have access to it.
---

Answer the question based on the above context: {question}

If the question is off-topic, answer the question but also ask the student if they have any computer programming questions.
"""

def main():
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        print("You must enter your API key.")
        return
    
     # Ask user for the question.
    query_text = input("Enter your question: ")

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if not results:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Generate prompt.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Invoke OpenAI model.
    model = ChatOpenAI()
    response = model.invoke(prompt)

    # Extract response text from the response object
    response_text = response.content.strip(' "')

    # Print the response text
    print("\nMetadata:")
    for doc, score in results:
        print(f"Document: {doc.metadata}")
        print(f"Relevance Score: {score}")
        print("Content:")
        print(doc.page_content)
        print("-"*20,"\n\n")
    print("*"*20)
    print(response_text)
    print("*"*20)

if __name__ == "__main__":
    main()
