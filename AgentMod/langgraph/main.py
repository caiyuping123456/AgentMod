from langchain_core.messages import HumanMessage

from AgentMod.langgraph.langGraph import getAgent

if __name__ == '__main__':
    agent = getAgent()
    initial_state = {
        "messages": [HumanMessage(content="你好，今天赣州的天气")]
    }

    final_state = agent.invoke(initial_state)
    last_message = final_state["messages"][-1]
    print(last_message.content)
