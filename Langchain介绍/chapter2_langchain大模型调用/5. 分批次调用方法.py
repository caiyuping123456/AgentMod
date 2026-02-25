"""
    分批次调用和同步异步方法
"""
# 标准的模型调用
import os

import dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME"),
)

messages1 = [
    SystemMessage(content="你是一个御姐"),
    HumanMessage(content="介绍Langchain")
]
messages2 = [
    SystemMessage(content="你是一个御姐"),
    HumanMessage(content="介绍AIGC")
]
messages3 = [
    SystemMessage(content="你是一个御姐"),
    HumanMessage(content="介绍大模型")
]
messages = [messages1, messages2, messages3]
# 分批次调用
re2 = chat.batch(messages)
print(re2)


