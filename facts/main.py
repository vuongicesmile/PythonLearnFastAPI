from langchain.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()

# làm cách nào để upload file
loader = TextLoader("facts.txt")

# load file trong txt ra
docs = loader.load()

print(docs)
