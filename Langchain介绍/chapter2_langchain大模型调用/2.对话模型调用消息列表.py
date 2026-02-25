# 标准的模型调用
import os

import dotenv
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)

# 调用大模型
User_message = "什么是langchain"
# ll = chat.invoke(User_message)
# print(ll.content)


"""
    在langchain中内置了5中消息
    1. SystemMessage：系统提示词
    2. HumanMessage：用户的输入
    3. AiMessage：存储Ai放回的内容
    4. ChatMessage：自定义角色通用消息信息
    5. FunctionMessage：函数调用
"""
# 写系统提示词
system_message = SystemMessage(content="你是一个御姐")

# 写用户消息
human_Message = HumanMessage(content="叫我帅哥")

messages = [system_message, human_Message]

print(messages)

# 调用大模型
# 这个是一个AiMessage
re = chat.invoke(messages)
print(re.content)


