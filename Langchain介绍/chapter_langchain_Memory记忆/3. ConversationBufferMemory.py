from langchain_classic.chains.llm import LLMChain
from langchain_classic.memory import ConversationBufferMemory
import os

import dotenv
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

# 使用配置文件方式
dotenv.load_dotenv() # 一定要加这个（使用配置文件）===> 加载配置文件
chat = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_NAME")
)

# 实例化ConversationBufferMemory()
# return_messages设置为true表示显示完整的：response_metadata
con = ConversationBufferMemory(return_messages=True)

# 添加消息
con.save_context(inputs={"input":"你好" },outputs={"output":"你好，很高兴认识你"})
con.save_context(inputs={"input":"回答一下1+2+3=?"},outputs={"output":"7"})

# 输出：方式1
print(con.load_memory_variables({}))

# 输出：方式2
print(con.chat_memory.messages)

template = """你可以与人类对话。
当前对话: {history}
人类问题: {question}
回复:
"""
prompt = PromptTemplate.from_template(template)
# 创建ConversationBufferMemory
memory = ConversationBufferMemory()
# 初始化链
chain = LLMChain(llm=chat, prompt=prompt, memory=con)
# 提问
res1 = chain.invoke({"question": "我问的数学问题是什么"})
print(res1)
print(con.load_memory_variables({}))
# 添加回答(必须是字典)
con.save_context(
    {"input": res1['question']},
    {"output": res1['text']}
)
chain2 = LLMChain(llm=chat, prompt=prompt, memory=con)

res2 = chain2.invoke({"question":'我问了什么问题？'})
print(res2)

# 当然，可以通过memory_key，进行修改
# con2 = ConversationBufferMemory(memory_key="res")


