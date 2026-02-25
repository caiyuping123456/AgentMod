import os
from langchain_anthropic import ChatAnthropic

# 1. 设置环境变量（也可以直接在初始化对象时传入）
os.environ["ANTHROPIC_API_KEY"] = "sk-8B26rOX7C1vLPJyEgnmxG8r0ixWk37U7KgEsHnACE9j8nv6o"

# 2. 初始化模型
# 注意：base_url 必须指向 API 的根路径（通常是 /v1）
llm = ChatAnthropic(
    model_name="mimo-v2-flash",
    anthropic_api_url="http://8.153.39.35:3003", # 对应你的 ANTHROPIC_BASE_URL
    timeout=None,
    stop=None,
)

# 3. 测试调用
response = llm.invoke("你好，请问你是谁？")
print(response.content)