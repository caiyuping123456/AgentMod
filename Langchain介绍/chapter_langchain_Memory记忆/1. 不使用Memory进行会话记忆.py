import os

import dotenv
from langchain_core.messages import SystemMessage, AIMessage
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

def chat_with_model():
    prompt_template = ChatPromptTemplate.from_messages([
        ("system","你是一个御姐，也是我老婆"),
        ("human","{question}")
    ])

    chat_model = prompt_template | chat
    while True:
        user_prompt = input("请输入你的问题(输入‘退出’时结束对话)")
        if(user_prompt == "退出") :
            print("用户已经选择退出")
            break;
        response = chat_model.invoke({"question":user_prompt})
        print("ai回复：",response.content)

        # 进行模型对话添加
        prompt_template.messages.append(HumanMessage(content=user_prompt))
        prompt_template.messages.append(AIMessage(content=response.content))


if __name__ == "__main__":
    print("对话开始了")
    chat_with_model()
