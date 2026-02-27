from typing import TypedDict, Annotated, Sequence

import dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import StateGraph, END

from AgentMod.tools.toos_map import ToolIocContainer
from AgentMod.tools.weather import weatherTool as weather
import os

dotenv.load_dotenv()
# 设置环境变量 (或者直接在代码中传入 api_key)
# os.environ["OPENAI_API_KEY"] = "your-key"

# 1. 定义工具
tool_path = r"D:\Py_Project\Langcahin\AgentMod\tools\tool_config.yaml"
ToolIocContainer.load_tool_config(tool_path)
tools = ToolIocContainer.get_tool()

llm = ChatNVIDIA(
    base_url=os.getenv("BASE_URL"),
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
)

llm_with_tools = llm.bind_tools(tools)


# 2. 定义 State (状态)
# TypedDict 用于定义共享数据的结构
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]


# 3. 定义节点函数
def chat_node(state: AgentState):
    messages = state["messages"]
    # 调用 LLM
    response = llm_with_tools.invoke(messages)
    # 更新状态：追加新的 AI 消息
    return {"messages": [response]}


def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    # 简单处理：假设最后一条消息包含工具调用
    # 在实际生产中，这里会解析 tool_calls 并执行对应工具
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        name = tool_call["name"]
        args = tool_call["args"]
        if name == "get_weather":
            result = weather.getWeather.invoke(args)
            tool_outputs.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))

    return {"messages": messages + tool_outputs}


# 4. 定义条件边逻辑
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    # 如果最后一条消息有 tool_calls，则继续执行工具节点
    if last_message.tool_calls:
        return "tools"
    # 否则结束
    return END


# 5. 构建图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", chat_node)
workflow.add_node("tools", tool_node)

# 设置入口点
workflow.set_entry_point("agent")

# 添加边
# 正常情况：agent -> 条件判断
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",  # 如果需要工具，去 tools 节点
        END: END  # 如果不需要，结束
    }
)

# 工具执行完后，必须回到 agent 节点 (形成循环)
workflow.add_edge("tools", "agent")

# 编译图
app = workflow.compile()

# 6. 运行
inputs = {"messages": [HumanMessage(content="北京天气怎么样？")]}
config = {"configurable": {"thread_id": "1"}}  # 用于持久化追踪

print("开始运行 Agent...")
# stream 可以实时看到每一步的输出
for event in app.stream(inputs, config):
    for key, value in event.items():
        print(f"--- 节点: {key} ---")
        print(value["messages"][-1].content if hasattr(value["messages"][-1], 'content') else "工具调用完成")
