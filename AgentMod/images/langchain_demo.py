from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 初始化模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key="your-api-key-here"  # 请替换为你的 API key
)

# 创建消息
message = HumanMessage(content="你好，请介绍一下你自己。")

# 调用模型
response = llm.invoke([message])

# 打印结果
print(f"AI回复: {response.content}")