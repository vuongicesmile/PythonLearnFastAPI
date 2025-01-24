from langchain.document_loaders import TextLoader
# dùng thư viện để chunk text trong file
from langchain.text_splitter import CharacterTextSplitter
# dùng thư viện để embedding các chuỗi vector
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeedings = OpenAIEmbeddings()

emb = embeedings.embed_query("hi there")

# tách chuỗi thành dãy mảng
print(emb)

# text_splitter = CharacterTextSplitter(
#   separator="\n",
#   chunk_size=200,
#   chunk_overlap=0
# )
# # làm cách nào để upload file -- sử dụng text loader
# loader = TextLoader("facts.txt")
# docs = loader.load_and_split(
#   text_splitter=text_splitter
# )



# # load file trong txt ra
# docs = loader.load()

# print(docs)
