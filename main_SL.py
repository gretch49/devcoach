import os
import streamlit as st
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Header
st.header("dev Coach")
st.subheader("A virtual tutor designed to assist students in learning coding through retrieval-augmented generation.", divider='rainbow')
st.caption('This is a string that explains something above.')
st.write_stream('This is a string that explains something above.')

MD_CHROMA_PATH = "data/chroma_md"  # Path for Markdown files
TXT_CHROMA_PATH = "data/chroma_txt"  # Path for text files
HTML_CHROMA_PATH = "data/chroma_html"  # Path for HTML files

# PROMPT_TEMPLATE = """
# You are a computer programming tutor. Answer the question based on the following context:

# {context}

# Don't reference the context in your response, because your student might not have access to it.
# ---

# Answer the question based on the above context: {question}

# If the question isn't related to tech, programming, computers, or software, answer the question but also ask the student if they have any computer programming questions. If the student is on-topic, just answer the question.
# """

# def main():
#     OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
#     if not OPENAI_API_KEY:
#         st.error("You must enter your API key.")
#         return

#     # Prepare the DB for Markdown files.
#     embedding_function = OpenAIEmbeddings()
#     md_db = Chroma(persist_directory=MD_CHROMA_PATH, embedding_function=embedding_function)

#     # Prepare the DB for text files.
#     txt_db = Chroma(persist_directory=TXT_CHROMA_PATH, embedding_function=embedding_function)

#     # Prepare the DB for HTML files.
#     html_db = Chroma(persist_directory=HTML_CHROMA_PATH, embedding_function=embedding_function)

#     # Initialize ChatOpenAI model.
#     model = ChatOpenAI()

#     st.title("AI Programming Tutor")

#     # Start the conversation loop.
#     while True:
#         # Ask user for the question.
#         query_text = st.text_input("Enter your question:")

#         # Check if the user wants to end the conversation.
#         if query_text.lower() == "bye":
#             st.write("Computer: Goodbye!")
#             break

#         elif query_text:
#             # Search the DB for Markdown files.
#             md_results = md_db.similarity_search_with_relevance_scores(query_text, k=3)
#             txt_results = txt_db.similarity_search_with_relevance_scores(query_text, k=3)
#             html_results = html_db.similarity_search_with_relevance_scores(query_text, k=3)

#             # Combine results from all databases
#             results = md_results + txt_results + html_results

#             if not results:
#                 st.write("Computer: Unable to find matching results.")
#                 continue

#             results = [(doc, score) for doc, score in results if score >= 0.8]

#             if not results:
#                 context_text = "\n\n---\n\n There is no context. Use your own knowledge."
#             else:
#                 context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

#             # Generate prompt.
#             prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#             prompt = prompt_template.format(context=context_text, question=query_text)

#             # Invoke OpenAI model.
#             response = model.invoke(prompt)

#             # Extract response text from the response object
#             response_text = response.content.strip(' "')

#             # Print the metadata and response text for each result
#             if results:
#                 st.write("\nMetadata:")
#                 for doc, score in results:
#                     st.write(f"Document: {doc.metadata}")
#                     st.write(f"Relevance Score: {score}")
#                     st.write("Content:")
#                     st.write(doc.page_content)
#                     st.write("-" * 20)

#             else:
#                 st.write("No matching results. I'll give you my best guess.")

#             st.write("*" * 20)
#             st.write(f"AI Tutor: {response_text}")
#             st.write("*" * 20)

# if __name__ == "__main__":
#     main()
