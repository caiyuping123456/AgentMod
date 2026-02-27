from typing import TypedDict, Sequence

from langchain_core.messages import BaseMessage
from langchain_core.messages.tool import tool_call, ToolMessage
from langgraph.constants import END
from langgraph.graph import StateGraph

from AgentMod.langgraph.langchain import getLLModel
from AgentMod.langgraph.tools import getTools

tools = getTools()
LLM_chat = getLLModel()
LLM_chat.bind_tools(tools)
tool_map = {t.name: t for t in tools}

##定义定义 State
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]

## 定义chat节点
def chat_node(state: AgentState):
    #获取到用户的信息
    messages = state["messages"]
    response = LLM_chat.invoke(messages)
    return {"messages":[response]}

##定义工具使用
def tool_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    tool_outputs = []
    for tool in last_message.tool_calls():
        name = tool["name"]
        args = tool["args"]
        tool_call_id = tool_call["id"]
        if name in tool_map:
            try:
                tool_call = tool_map[name]
                result = tool_call.invoke(args)
                tool_outputs.append(
                    ToolMessage(content=str(result), tool_call_id=tool_call_id)
                )
            except Exception as e:
                error_msg = f"工具执行出错: {str(e)}"
                tool_outputs.append(
                    ToolMessage(content=error_msg, tool_call_id=tool_call_id)
                )
        else:
            error_msg = f"未找到名为 '{name}' 的工具。可用工具: {list(tool_map.keys())}"
            tool_outputs.append(
                ToolMessage(content=error_msg, tool_call_id=tool_call_id)
            )
    return {"messages":tool_outputs}

## 定义边的逻辑
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

def getAgent():
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
    return workflow.compile()