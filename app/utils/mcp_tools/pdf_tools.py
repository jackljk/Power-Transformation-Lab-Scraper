from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS  # or Chroma
from langchain.embeddings import OpenAIEmbeddings
import pymupdf4llm