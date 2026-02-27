from typing import TypedDict, Annotated, Sequence
import dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import StateGraph, END
from AgentMod.tools.toos_map import ToolIocContainer
import os

dotenv.load_dotenv()

# 1. 定义工具
tool_path = r"D:\Py_Project\Langcahin\AgentMod\tools\tool_config.yaml"
ToolIocContainer.load_tool_config(tool_path)
tools = ToolIocContainer.get_tool()

# 【重要】创建一个工具名称到工具对象的映射字典，方便动态查找
# 这样就不需要写一堆 if-else 了
tool_map = {t.name: t for t in tools}

print(f"已加载工具: {list(tool_map.keys())}")

llm = ChatNVIDIA(
    base_url=os.getenv("BASE_URL"),
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
    max_completion_tokens=2048,  # 【关键】增加输出长度，防止生成代码时截断
    temperature=0.1  # 降低温度，让代码生成更稳定
)

llm_with_tools = llm.bind_tools(tools)


# 2. 定义 State (状态)
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]


# 3. 定义节点函数
def chat_node(state: AgentState):
    messages = state["messages"]
    print(f"\n[AI 思考中...] 当前对话轮数: {len(messages)}")

    # 调用 LLM
    response = llm_with_tools.invoke(messages)

    # 简单日志
    if response.tool_calls:
        tool_names = [tc['name'] for tc in response.tool_calls]
        print(f">> 决定调用工具: {tool_names}")
    else:
        content_preview = response.content[:50] + "..." if len(response.content) > 50 else response.content
        print(f">> 最终回复: {content_preview}")

    return {"messages": [response]}


def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    tool_outputs = []

    # 遍历所有需要调用的工具
    for tool_call in last_message.tool_calls:
        name = tool_call["name"]
        args = tool_call["args"]
        tool_call_id = tool_call["id"]

        print(f"   -> 正在执行工具: {name}, 参数: {args}")

        # 【核心修改】动态查找并执行工具
        if name in tool_map:
            try:
                target_tool = tool_map[name]
                # invoke 方法通常接受字典作为参数
                result = target_tool.invoke(args)

                # 将结果封装为 ToolMessage
                tool_outputs.append(
                    ToolMessage(content=str(result), tool_call_id=tool_call_id)
                )
                print(f"   <- 工具执行成功 (返回长度: {len(str(result))})")
            except Exception as e:
                error_msg = f"工具执行出错: {str(e)}"
                print(f"   <- 错误: {error_msg}")
                # 即使出错也要返回消息，让 AI 知道失败了，它可以尝试重试
                tool_outputs.append(
                    ToolMessage(content=error_msg, tool_call_id=tool_call_id)
                )
        else:
            error_msg = f"未找到名为 '{name}' 的工具。可用工具: {list(tool_map.keys())}"
            print(f"   <- 错误: {error_msg}")
            tool_outputs.append(
                ToolMessage(content=error_msg, tool_call_id=tool_call_id)
            )

    # 返回包含工具执行结果的消息列表
    return {"messages": tool_outputs}


# 4. 定义条件边逻辑
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    # 检查是否有工具调用
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END


# 5. 构建图
workflow = StateGraph(AgentState)

workflow.add_node("agent", chat_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

app = workflow.compile()

# 6. 运行
if __name__ == "__main__":
    # 测试任务：读取文件并写代码
    task = "D:\\Py_Project\\Langcahin\\AgentMod\\images\\text.md 文件是一个算法题，请你读取里面的内容，写一个完整的 Python Demo (LRU 缓存)，保存到同目录下。"

    inputs = {"messages": [HumanMessage(content=task)]}
    config = {"configurable": {"thread_id": "lru_demo_01"}}

    print("=" * 30)
    print("开始运行 LangGraph Agent...")
    print("=" * 30)

    try:
        for event in app.stream(inputs, config):
            for key, value in event.items():
                # 这里可以添加更详细的节点输出监控
                pass

        print("\n" + "=" * 30)
        print("✅ 任务流程结束！请检查文件是否生成。")
        print("=" * 30)

        # 打印最后一条 AI 的总结
        final_messages = value.get("messages", [])
        for msg in reversed(final_messages):
            if isinstance(msg, HumanMessage): continue
            if isinstance(msg, ToolMessage): continue
            if hasattr(msg, 'content') and msg.content:
                print(f"🤖 AI 总结:\n{msg.content}")
                break

    except Exception as e:
        print(f"\n❌ 发生严重错误: {e}")
        import traceback

        traceback.print_exc()