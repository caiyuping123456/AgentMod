"""\
    大数据输出的将其装维合适的

    str_outputparse
"""
import os

import dotenv
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)

re1 = chat.invoke("什么是大模型？")

## 1. 字符串解析器
### 方式1：
print("content:",re1.content)
### 方式2：
str1 = StrOutputParser()
re11 = str1.invoke(re1)
print("stroutputparser",re11)

## 2. json解析器
chat_message = ChatPromptTemplate.from_messages([
    ("system","你是一个{role}"),
    ("human","{question}")
])

ll = chat_message.invoke(input = {"role":"我女朋友","question":"什么是大模型?,返回一个json格式，q表示问题，a表示答案"})
re2 = chat.invoke(ll)
### 注意，一定要放回Json格式
print("json:",re2.content)
json = JsonOutputParser()
json11 = json.invoke(re2)

print(json11)

# 方式2 使用自带的格式进行回复
json2 = JsonOutputParser()
prompt = PromptTemplate.from_template(
    template="回答的格式是：{format},回答的问题是：{question}",
    partial_variables = {"format":json2.get_format_instructions()}
)
ll3 = prompt.invoke({"question":"什么是LLM?"})
re3 = chat.invoke(ll3)
json12 = json2.invoke(re3)
print(json12)

# 写法2 (链式调用)
chain = prompt | chat | json2
json_result = chain.invoke({"question":"什么是LLM?"})
print(json_result)