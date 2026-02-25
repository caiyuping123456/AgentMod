import os

import dotenv
from langchain_openai import ChatOpenAI

#获取大模型
# chat = ChatOpenAI(
#     base_url="http://8.153.39.35:3003/v1",  # 注意加上 /v1
#     api_key="sk-8B26rOX7C1vLPJyEgnmxG8r0ixWk37U7KgEsHnACE9j8nv6o",
#     model="mimo-v2-flash"
# )
# 2. 使用环境变量方式
# # chat = ChatOpenAI(
# #     base_url="http://8.153.39.35:3003/v1",  # 注意加上 /v1
# #     api_key=os.environ["CHAT_API_KEY"],
# #     model=os.environ["CHAT_MODEL_NAME"]
# # )
# 3. 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)
# 4. 使用配置文件方式
# dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
#
# os.environ["API_KEY"] = os.getenv("API_KEY")
# os.environ["BASE_URL"] = os.getenv("BASE_URL")
#
# chat = ChatOpenAI(
#     model = os.getenv("MODEL_NAME")
# )
# 调用大模型
User_message = "什么是langchain"
ll = chat.invoke(User_message)
print(ll.content)