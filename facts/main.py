from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
import time
from tenacity import retry, wait_random_exponential, stop_after_attempt

load_dotenv()

# Khởi tạo ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini", 
)

# Khởi tạo OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Hàm retry để xử lý lỗi RateLimitError
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def embed_query_with_retry(query):
    return embeddings.embed_query(query)

emb = embed_query_with_retry("hi there")

# Cấu hình TextSplitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

# Sử dụng TextLoader để tải file
try:
    loader = TextLoader("facts.txt")
    docs = loader.load_and_split(text_splitter=text_splitter)
except FileNotFoundError:
    print("File 'facts.txt' không tồn tại. Vui lòng kiểm tra lại đường dẫn.")
    exit()

# Tạo Chroma VectorStore với retry
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def create_chroma_db():
    return Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory="emb"
    )

db = create_chroma_db()

# Tìm kiếm dựa trên độ tương đồng
query = "what is an interesting fact about the English language?"
results = db.similarity_search_with_score(query)

# In kết quả
for result in results:
    print("\n")
    print(f"Score: {result[1]}")
    print(f"Content: {result[0].page_content}")
