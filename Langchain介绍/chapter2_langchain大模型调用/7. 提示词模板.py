"""
PromptValue-Template 提示词模板

    PromptTemplate：LLM提示模板，用于生成字符串提示词
    ChatPromptTemplate：聊天提示词模板，用于各种角色的提示词模板，传入大模型
    XxMessagePromptTemplate：消息模板词模板，
    FewShotPromptTemplate：样本提示词模板，教大模型如何回答
    PiplinePromplate：管道提示词模板
    自定义模板
"""
from langchain_core.prompts import PromptTemplate

# PromptTemplate的使用
# 1. PromptTemplate如何获取实例
##   a.通过构造方法
pro1 = PromptTemplate(
    template="你是{role},名字是{name}",
    input_variables=["role","name"]
)
## 填充
re1 = pro1.format(role="美女",name="哈哈")
print(re1)


##   b.使用format_template()方法 （推荐）
pro2 = PromptTemplate.from_template(template="你是{role},名字是{name}")
## 填充
re2 = pro2.format(role="美女",name="哈哈")
print(re2)

##   c.不用填充
text = """
    我是帅哥
"""
pro3 = PromptTemplate.from_template(text)
## 填充
re3 = pro3.format()
print(re3)


"""
    两种特殊结构的使用
        1. 部分提示词模板（重点）
        2. 组合提示词的使用
"""
#部分提示词模板（重点）
pro4 = PromptTemplate(
    template="你是{role},名字是{name}",
    partial_variables={"role":"美女"}# 部分提示词的使用
)
#也可以调用partial进行填充
pro4 = pro4.partial(name = "xixi") # 不会对本身进行修改
## 填充
re4 = pro4.format()
print(re4)

#组合提示词的使用
template = (
    PromptTemplate.from_template(text)+
    "你好"+
    "name={name}"
)
re5 = template.format(name="haha")
print(re5)

"""
    给变量赋值的两种方式：
        1. fromat():放回值是String类型
        2. invoke():参数是dic类型，输出是PromptValue类型
"""
pro5 = PromptTemplate(
    template="你是{role},名字是{name}",
    input_variables=["role","name"]
)
## 填充
re5 = pro5.invoke(input={"role":"美女","name":"哈哈"})
print(re5)

#结合大模型
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
pro6 = PromptTemplate(
    template="你是{role},名字是{name}，请介绍一下你自己",
)
## 填充
re6 = pro6.invoke(input={"role":"喵娘","name":"燕"})
# 分批次调用
response1 = chat.invoke(re6)
print(response1)


