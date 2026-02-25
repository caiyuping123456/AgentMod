from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def run_siliconflow_call():
    """
    使用 LangChain 的 ChatOpenAI 类，通过指定 base_url 来调用硅基流动 API 的示例。
    """
    # ⚠️ 替换为您真实的 API 密钥 (从硅基流动平台获取)
    SILICONFLOW_API_KEY = "sk-eejpytshnxihqbeedqsgfuixodazjxjxjetbounsqbzzygtr"

    # ⚠️ 替换为硅基流动 API 的实际基础 URL/端点
    # (您需要从硅基流动的 API 文档中查找此地址)
    SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"

    # ⚠️ 替换为您在硅基流动平台上可用的模型名称
    SILICONFLOW_MODEL_NAME = "Qwen/Qwen3-8B"

    if "YOUR_ACTUAL_SILICONFLOW_API_KEY_HERE" in SILICONFLOW_API_KEY:
        print("错误：请将 SILICONFLOW_API_KEY 替换为您真实的 API 密钥。")
        return
    if "YOUR_SILICONFLOW_API_BASE_URL_HERE" in SILICONFLOW_BASE_URL:
        print("错误：请将 SILICONFLOW_BASE_URL 替换为硅基流动的实际 API 端点。")
        return

    try:
        # 1. 初始化 Chat 模型
        # 使用 ChatOpenAI 类，但通过 openai_api_base 指向硅基流动的 API 端点
        model = ChatOpenAI(
            model=SILICONFLOW_MODEL_NAME,
            api_key=SILICONFLOW_API_KEY,
            openai_api_base=SILICONFLOW_BASE_URL
        )

        # 2. 定义聊天消息
        system_msg = SystemMessage("你是一个乐于助人的助手，请用简洁的中文回答问题。")
        human_msg = HumanMessage("请问硅基流动提供的主要 AI 服务有哪些？")

        messages = [system_msg, human_msg]

        print("--- 正在调用 硅基流动 API ---")

        # 3. 调用模型
        response = model.invoke(messages)

        # 4. 打印结果
        print("--- 成功获取响应 ---")
        print(f"模型回复:\n{response.content}")

    except Exception as e:
        print("\n--- API 调用失败 ---")
        print(f"详细错误信息: {e}")


if __name__ == "__main__":
    run_siliconflow_call()