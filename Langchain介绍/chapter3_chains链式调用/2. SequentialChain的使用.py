"""
    SequentialChain允许多个输入和多个输出
    注意，多个输出表示不是最后的结果输出多个，是表示过程中的链也可以做为输出
    同样，多个输入也表示在调用链之前，可以在输入之后再进行输入
"""
## 举例如下：
import os

import dotenv
from langchain_core.messages import SystemMessage
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

schainA_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一位精通各领域知识的知名教授"),
        ("human","请你先尽可能详细的解释一下：{knowledge}，并且{action}")
    ]
)
schainA_chains = LLMChain(llm=chat,
                          prompt=schainA_template,
                          verbose=True,
                          output_key="schainA_chains_key"
                          )
# schainA_chains.invoke({
#     "knowledge": "中国的篮球怎么样？",
#     "action": "举一个实际的例子"
# }
# )
schainB_template = ChatPromptTemplate.from_messages(
    [
        ("system","你非常善于提取文本中的重要信息，并做出简短的总结"),
        ("human","这是针对一个提问完整的解释说明内容：{schainA_chains_key}"),
        ("human","请你根据上述说明，尽可能简短的输出重要的结论，请控制在100个字以内"),
    ]
)
schainB_chains = LLMChain(llm=chat,
                         prompt=schainB_template,
                         verbose=True,
                         output_key='schainB_chains_key'
                          )
Seq_chain = SequentialChain(
                            chains=[schainA_chains, schainB_chains],
                            input_variables=["knowledge","action"],
                            output_variables=["schainA_chains_key","schainB_chains_key"],
                            verbose=True)
response = Seq_chain.invoke({"knowledge":"中国足球为什么踢得烂","action":"举一个实际的例子"})
print(response)