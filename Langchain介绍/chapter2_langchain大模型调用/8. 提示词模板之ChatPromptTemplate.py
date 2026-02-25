# PromptTemplate实例化
# 两种：一种是构造函数，一种是from_message()
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, \
    MessagesPlaceholder

chatpro1 = ChatPromptTemplate(
    messages=[
        ("system","你是一个Ai助手,名字是：{name}"),
        ("human","我的问题是：{question}")
    ],
    input_variables=["name","question"]
)
re1 = chatpro1.invoke({"name":"小明","question":"1+1+2+3=?"})
print(re1)
print(re1.messages)

chatpro2 = ChatPromptTemplate.from_messages([
        ("system","你是一个Ai助手,名字是：{name}"),
        ("human","我的问题是：{question}")
])
re2 = chatpro2.invoke({"name":"小明","question":"1+1+2+3=?"})
print(re2)
print(re2.messages)

# 调用提示词模板的几种方式：invoke(),format(),format_message(),format_prompt()

# 举例：invoke()
re3 = chatpro2.invoke({"name":"小红","question":"1+1+2+3=?"})
print(re3)
print(type(re3))# <class 'langchain_core.prompt_values.ChatPromptValue'>

# 举例：format()
re4 = chatpro2.format(name="小蔡",question="1+1+2+3=?")
print(re4)
print(type(re4))# <class 'str'>

# 举例：format_message()
re5 = chatpro2.format_messages(name="小燕",question="1+1+2+3=?")
print(re5)
print(type(re5))# <class 'list'>

# 举例：format_prompt()
re6 = chatpro2.format_prompt(name="小一",question="1+1+2+3=?")
print(re6)
print(type(re6))# <class 'langchain_core.prompt_values.ChatPromptValue'>

# ChatPromptValue转为list和Str
# 转为list
re6_message = re6.to_messages()
print(re6_message)
print(type(re6_message))

# 转为str
re6_str = re6.to_string()
print(re6_str)
print(type(re6_str))

# 更加丰富的实例化构造参数
#可以使用字符串，字典，列表，元组，Chat提示词模板，消息提示词模板。
## 字符串
chatpro3 = ChatPromptTemplate.from_messages([
    "我的问题是：{question}"
])
re7 = chatpro3.format(question="哈哈哈哈")
print(re7)

## 字典
chatpro4 = ChatPromptTemplate.from_messages([
    {"role":"system","content":"我是一个美女，我叫{name}"},
    {"role":"human","content":"我的问题是：{question}"}
])
re8 = chatpro4.invoke(input={"name":"燕","question":"什么是大模型"})
print(re8.messages)

## 消息类型
chatpro5 = ChatPromptTemplate.from_messages([
    SystemMessage(content="我是一个美女，我叫{name}"),
    HumanMessage(content="我的问题是：{question}")
])
re9 = chatpro5.format(name="燕",question="1+1+2+3=?")
print(re9)

## 消息提示词模板
system_message = "我是一个美女，我叫{name}"
SystemMessage = SystemMessagePromptTemplate.from_template(system_message)
human_message = "我的问题是：{question}"
HumanMessage = HumanMessagePromptTemplate.from_template(human_message)
chatpro6 = ChatPromptTemplate.from_messages([
    SystemMessage,
    HumanMessage
])
re10 = chatpro6.format(name="燕",question="1+1+2+3=?")
print(re10)

### 可以看到这里的消息类型和消息提示词的区别，消息类型传入的就是一个字符串，不能进行赋值，
### 而使用消息提示词的就可以进行赋值

# 结合LLM
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
system_message7 = "我是一个美女，我叫{name}"
SystemMessage7 = SystemMessagePromptTemplate.from_template(system_message)
human_message7 = "我的问题是：{question}"
HumanMessage7 = HumanMessagePromptTemplate.from_template(human_message)
chatpro7 = ChatPromptTemplate.from_messages([
    SystemMessage7,
    HumanMessage7
])
## 填充
re11 = chatpro7.invoke({"name":"燕","question":"什么是大模型"})
llm1 = chat.invoke(re11)
print(llm1.content)


# 插入消息列表
## 如果你不知道需要插入什么角色，可以使用插入消息列表
chatpro8 = ChatPromptTemplate.from_messages([
    {"role":"system","content":"我是一个美女，我叫{name}"},
    MessagesPlaceholder("msg")
])
# msg=[HumanMessage(content="什么是java？")],里面就是一个列表AiMessage这些都可以传
re12 = chatpro8.format_messages(msg=[HumanMessage(content="什么是java？")],name="蔡")
llm2 = chat.invoke(re12)
print(llm2.content)
