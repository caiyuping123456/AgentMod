import asyncio
import json
import websockets
import datetime  # 新增：用于显示时间戳
from langchain_core.messages import HumanMessage
from AgentMod.langgraph.langGraph import getAgent  # 你的Agent模块

# -------------------------- 配置项 --------------------------
# NapCat反向WebSocket地址（和NapCat配置一致）
WS_URL = "ws://127.0.0.1:8080/onebot/v11/ws"
# 监听端口（和NapCat配置的反向WS端口一致）
LISTEN_PORT = 8081
# 允许接收的QQ群/好友（all=全部，也可填"115269573,123456"指定群/好友）
ALLOWED_TARGETS = "all"

# 初始化Agent
agent = getAgent()


# OneBot V11协议处理
async def handle_napcat_message(websocket):
    """处理NapCat推送的QQ消息，调用Agent并回复"""
    async for message in websocket:
        # 1. 解析NapCat推送的JSON消息
        try:
            msg_data = json.loads(message)
        except json.JSONDecodeError:
            continue

        # 只处理私聊/群聊消息（过滤其他事件）
        if msg_data.get("post_type") != "message":
            continue

        # ========== 新增：实时打印收到的原始消息（带时间戳） ==========
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_type = msg_data.get("message_type")  # private/group
        user_id = str(msg_data.get("user_id"))
        user_name = msg_data.get("sender", {}).get("nickname", "未知用户")  # 获取发送者昵称
        group_id = str(msg_data.get("group_id")) if message_type == "group" else ""
        group_name = msg_data.get("group_name", "")  # 获取群名（NapCat需开启相关配置）
        raw_message = msg_data.get("raw_message", "").strip()

        # 实时显示收到的消息
        if message_type == "group":
            print(
                f"\n[{current_time}]收到群聊消息 | 群：{group_name}({group_id}) | 发送人：{user_name}({user_id}) | 内容：{raw_message}")
        else:
            print(f"\n[{current_time}]收到私聊消息 | 发送人：{user_name}({user_id}) | 内容：{raw_message}")

        # 检查是否@机器人（只回复@的消息）
        at_me = False
        if 'message' in msg_data and isinstance(msg_data['message'], list):
            for item in msg_data['message']:
                if item.get('type') == 'at' and item.get('data', {}).get('qq') == str(msg_data.get('self_id')):
                    at_me = True
                    break
        if not at_me:
            print(f"[{current_time}] 未@机器人，跳过回复")
            continue

        # 过滤消息（仅处理指定目标）
        if ALLOWED_TARGETS != "all":
            target_id = group_id if group_id else user_id
            if target_id not in ALLOWED_TARGETS.split(","):
                print(f"[{current_time}] 非允许的目标({target_id})，跳过回复")
                continue

        # 空消息过滤
        if not raw_message:
            print(f"[{current_time}] 空消息，跳过回复")
            continue

        # 调用Agent生成回复（带加载提示）
        print(f"[{current_time}] 正在调用Agent生成回复...")
        try:
            initial_state = {"messages": [HumanMessage(content=raw_message)]}
            final_state = agent.invoke(initial_state)
            ai_response = final_state["messages"][-1].content
        except Exception as e:
            ai_response = f"Agent调用出错：{str(e)}"
            print(f"[{current_time}]Agent调用失败：{str(e)}")

        # 构造回复消息（OneBot V11协议）
        reply_data = {
            "action": "send_msg",
            "params": {
                "message_type": message_type,
                "message": ai_response,
                "user_id": user_id if message_type == "private" else "",
                "group_id": group_id if message_type == "group" else "",
                "auto_escape": False
            },
            "echo": msg_data.get("message_id")  # 消息回声，用于匹配回复
        }

        # 发送回复到NapCat
        await websocket.send(json.dumps(reply_data))

        # ========== 实时显示回复的消息 ==========
        print(f"[{current_time}]回复消息 | 内容：{ai_response[:100]}..." if len(
            ai_response) > 100 else f"[{current_time}]回复消息 | 内容：{ai_response}")


# -------------------------- 启动WebSocket服务 --------------------------
async def main():
    # 启动WebSocket服务器，监听NapCat的反向连接（绑定0.0.0.0避免连接问题）
    async with websockets.serve(
            handle_napcat_message,
            "0.0.0.0",  # 改为0.0.0.0，解决握手超时/连接拒绝问题
            LISTEN_PORT,
            ping_interval=15,  # 新增：心跳间隔，避免连接断开
            ping_timeout=30  # 新增：心跳超时
    ):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}]NapCat-AGENT服务已启动")
        print(f"[{current_time}]监听地址：ws://0.0.0.0:{LISTEN_PORT}")
        print(f"[{current_time}请确保NapCat的反向WebSocket配置为：ws://127.0.0.1:{LISTEN_PORT}/onebot/v11/ws")
        # 保持服务运行
        await asyncio.Future()


if __name__ == "__main__":
    # 禁用所有调试器干扰
    import os

    os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
    os.environ["PYTHONUNBUFFERED"] = "1"
    # 运行主程序
    asyncio.run(main())