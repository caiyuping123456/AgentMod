"""
    invoke()/stream()

    表示分批调用
    batch()

    表示异步调用
    ainvoke()/astream()/abacth()

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
    streaming=True # 开启流式调用
)
system_message = SystemMessage(content="你是一个御姐")
human_Message1 = HumanMessage(content="介绍Langchain")
messages = [system_message, human_Message1]

# 阻塞式调用
# re1 = chat.invoke(messages)
# print(re1.content)

# 流式调用
# 需要开启流式
re2 = chat.stream(messages)
for item in re2:
    print(item.content,end="",flush=True) # 刷新缓存区
print("流式调用结束")


