
#Sử dụng ChatOpenAI từ LangChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
# để ghép các chuỗi sử dụng SequentialChain 
from langchain.chains import LLMChain, SequentialChain
# không để public key ra ngoài, để trong env
from dotenv import load_dotenv
import argparse

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task", default="Return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()


# OpenAI đã ngừng hỗ trợ model text-davinci-003. Để khắc phục, bạn cần sử dụng các model mới hơn, như gpt-3.5-turbo hoặc gpt-4
llm = ChatOpenAI(
    model="gpt-4o-mini", 
)

code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"]
)

test_prompt = PromptTemplate(
    input_variables=["language", "code"],
    template="Write a test for the following {language} code:\n{code}"
)

code_chain = LLMChain(
    llm=llm,
    prompt=code_prompt,
    output_key="code"
)

test_chain = LLMChain(
    llm=llm,
    prompt=test_prompt,
    output_key="test"
)

chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["task", "language"],
    output_variables=["test", "code"]
)

# sửa theo argument truyền vô hiện tại
result =chain({
    "language": args.language,
    "task": args.task
})

print(">>>>>> GENERATED CODE:")
print(result["code"])

print(">>>>>> GENERATED TEST:")
print(result["test"])
