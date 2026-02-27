import os
import dotenv
from langchain_classic.agents import initialize_agent, AgentType
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from AgentMod.prompt.systemPrompt import SystemPromptTemple as SystemPrompt
from AgentMod.tools.toos_map import ToolIocContainer
from AgentMod.utils import logging as log

dotenv.load_dotenv()

# model_kwargs = {
#     "top_k": 40,  # GLM-5 专属参数
#     "repetition_penalty": 1.05,  # GLM-5 专属参数
#     "timeout": 20,  # 超时参数（模型专属）
# }

chat = ChatNVIDIA(
    base_url=os.getenv("BASE_URL"),
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
    # temperature=0.01,  # GLM-5 最优低随机性
    # top_p=0.6,  # 缩小采样范围
    max_completion_tokens=2048,
    # model_kwargs=model_kwargs,
)

#获取tool
## 注意被tool修饰的，使用时不用加（）
# tools = [weather.getWeather]
# functions = [convert_to_openai_function(i) for i in tools]
tool_path = r"D:\Py_Project\Langcahin\AgentMod\tools\tool_config.yaml"
ToolIocContainer.load_tool_config(tool_path)
tools = ToolIocContainer.get_tool()

# 获取系统提示
systemMessage = SystemPrompt.getSystemPromptTemplate()

humanMessage = HumanMessagePromptTemplate.from_template(
    template="{question}"
)

chatPrompt = ChatPromptTemplate.from_messages([
    systemMessage,humanMessage
])

# log.info("开始建立chain调用")
# chain = chatPrompt | chat
#
#
#
# log.info("开始进行生成回复")
# re = chain.invoke(
#     input={"question":"赣州市南康区现在的天气"},
#     functions = functions
# )

# 创建agent
log.info("开始进行创建agent")
agent = initialize_agent(
    tools=tools,
    llm=chat,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"prompt": chatPrompt},
    verbose=False # 是否打印详细执行过程
)

# your_question = "赣州市南康区现在的天气"
#
# 按模板参数格式传入（key必须是question，匹配你的{question}）
# result = agent.run({"question": your_question})
result = agent.invoke(r"D:\Py_Project\Langcahin\AgentMod\images\text.md文件是一个算法题，请你读取里面的内容，写一个Demo,写到同目录下（用python写）")
print(result.get("output"))

