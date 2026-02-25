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
    model=os.getenv("MODEL_NAME")
)

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
human_Message1 = HumanMessage(content="叫我帅哥")

messages = [system_message, human_Message1]

# 调用大模型
# 这个是一个AiMessage
re = chat.invoke(messages)
print(re.content)

# 多轮对话
ai_message = AIMessage(content=re.content)
human_Message2 = HumanMessage(content="你之前见我什么？现在叫我老公")
messages.append(ai_message)
messages.append(human_Message2)

re2 = chat.invoke(messages)
print(re2.content)


