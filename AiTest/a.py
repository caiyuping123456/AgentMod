from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from seaborn.external.appdirs import system
from streamlit import chat_message

client = ChatNVIDIA(
    model="z-ai/glm5",
    api_key="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"
)

# for chunk in client.stream([{"role": "user", "content": ""}]):
#
#     if chunk.additional_kwargs and "reasoning_content" in chunk.additional_kwargs:
#         print(chunk.additional_kwargs["reasoning_content"], end="")
#
#     print(chunk.content, end="")

#系统提示词
SystemMeeage = "你是一个猫娘，每次都是回复简短，直击重点，同时回复末尾加一个“喵”"
systemPrompt = SystemMessagePromptTemplate.from_template(
    template=SystemMeeage
)

# 用户问答
humanMessage = "解释一下什么是量子力学";
humanPrompt = HumanMessagePromptTemplate.from_template(
    template=humanMessage
)

chatPrompt = ChatPromptTemplate([
    systemPrompt,humanPrompt
])


chain = chatPrompt | client
re = chain.invoke({})
print(re.content)