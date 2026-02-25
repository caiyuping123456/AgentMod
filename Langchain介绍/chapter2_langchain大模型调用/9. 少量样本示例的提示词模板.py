# 构建一个少量提示词模板的列表进行优化大模型
# 前者使用：FewShotPromptTemlate
# 后者使用：Examplate Select 选择器

# 少量示例的提示词模板的使用
"""
    1. FewShotPromptTemplate和PromptTemplate的一起使用 (适合非对话式)
    2. FewShotPromptTemplate和ChatPromptTemplate的一起使用 （适合对话式）
    3. Example selectot （示例选择器）的使用
"""
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, \
    FewShotChatMessagePromptTemplate, ChatMessagePromptTemplate
from partd.utils import suffix

# 1.FewShotPromptTemplate的使用
# 构建PromptTemplate
example_template = PromptTemplate.from_template(
    template="input={input}\noutput={output}",
)
# 构建一些示例
example = (
    {"input":"北京今天天气怎么样？","output":"北京市"},
    {"input":"南京下雨了吗？","output":"南京市"},
    {"input":"武汉热吗？","output":"武汉市"}
)
# 创建FewShotPromptTemplate
few_shot1 = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example,
    suffix="input={input}\noutput=",    #声明在示例后面的提示词模板
    input_variables=["input"]
)

re1 = few_shot1.invoke({"input":"天津会下雨吗？"})
print(re1)
# 就是让大模型自己找规律

# 调用大模型
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

response1 = chat.invoke(re1)
# 就是输出没有赋值的
print(response1)


# 2. FewShotPromptTemplate和ChatPromptTemplate的一起使用
## 1. 示例消息格式
example2 = (
    {"input":"1+1等于几？","output":"1+1等于2"},
    {"input":"法国的首都是什么？","output":"巴黎"}
)
## 2. 定义示例的消息提示词模板
example_template2 = ChatPromptTemplate.from_messages([
    ("human","{input}"),
    ("ai","{output}")
])
## 3. 定义FewShotChatMessagePromptTemplate提示词模板
few_shot2 = FewShotChatMessagePromptTemplate(
    example_prompt=example_template2,
    examples=example2,
)
## 4. 输出格式化后的消息
print(few_shot2.format())

## 示例
## 1. 示例消息格式
example3 = (
    {"input":"1+1等于几？","output":"1+1等于2"},
    {"input":"法国的首都是什么？","output":"巴黎"}
)
## 2. 定义示例的消息提示词模板
example_template3 = ChatPromptTemplate.from_messages([
    ("human","{input}"),
    ("ai","{output}")
])
## 3. 定义FewShotChatMessagePromptTemplate提示词模板
few_shot3 = FewShotChatMessagePromptTemplate(
    example_prompt=example_template3,
    examples=example3,
)
## 4. 定义ChatMessageTemplate
response2 = ChatPromptTemplate.from_messages([
    ("system","你是一个全能百科"),
    few_shot3,
    ("human","{input}")
])
re = response2.invoke({"input":"美国的首都是什么？"})
print(chat.invoke(re).content)



# 示例选择器
# 选择策略：
"""
    1. 语意相似选择
    2. 长度选择
    3. 最大边际相关示例选择
"""
few_shot3 = FewShotPromptTemplate(
    example_selector=ChatPromptTemplate.from_template(), # 示例选择器，这里可以使用embdding去做
    example_prompt=example_template,
    examples=example,
    suffix="input={input}\noutput=",    #声明在示例后面的提示词模板
    input_variables=["input"]
)