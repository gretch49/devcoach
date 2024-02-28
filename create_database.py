import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

DATA_PATH = "data"
CHROMA_PATH_HTML = os.path.join(DATA_PATH, "chroma_html")
CHROMA_PATH_MD = os.path.join(DATA_PATH, "chroma_md")
CHROMA_PATH_TXT = os.path.join(DATA_PATH, "chroma_txt")

def main():
    # Remove existing database directories
    remove_database_dirs([CHROMA_PATH_HTML, CHROMA_PATH_MD, CHROMA_PATH_TXT])
    
    # Generate new data store
    generate_data_store()

def remove_database_dirs(paths):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)

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
    # Create a new database from the chunks.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=chroma_path
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {chroma_path}.")
    print(f"Added {num_files} files to the database.")

if __name__ == "__main__":
    main()
