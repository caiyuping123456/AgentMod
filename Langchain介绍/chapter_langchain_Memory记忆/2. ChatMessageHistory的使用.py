import os

import dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)

"""
    记忆存储：ChatMessageHistory
"""
# 创建ChatMessageHistory实例
history = ChatMessageHistory()

# 添加消息
history.add_message("你好")
history.add_ai_message("你好")
history.add_message("你是我老婆")
history.add_ai_message("好的，老公")
history.add_message("你叫我老公了吗")

print(history.messages)

# 调用大模型
response= chat.invoke(history.messages)
print(response.content)