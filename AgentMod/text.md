LangChain AgentType 核心对比表（结合天气查询场景）
表格
AgentType 枚举值（官方标准）	核心特性	关键限制	天气查询场景示例	选型建议
1. OPENAI_FUNCTIONS	✅ 适配 OpenAI 模型原生函数调用格式
✅ 自动生成标准化 JSON 工具调用指令
✅ 支持多参数工具	❌ 仅适配 OpenAI/GPT 系列模型
❌ 你的 NVIDIA 模型无法使用	（仅 OpenAI 模型可用）
提问：“查南康区天气”
Agent 返回：
{"name":"getWeather","parameters":{"lat":25.65,"lon":114.77}}	仅当使用 OpenAI 模型时选择，你的场景❌不推荐
2. ZERO_SHOT_REACT_DESCRIPTION（零样本推理）	✅ 零样本（无示例也能解决新问题）
✅ 所有模型通用（含 NVIDIA）
✅ 逻辑简单、运行快	❌ 仅支持单参数工具
❌ 无法处理 lat+lon 双参数	（需改造工具为单参数）
工具参数：city（仅城市名）
提问：“查南康区天气”
Agent 调用：getWeather(city="南康区")	仅当工具为单参数时选择，你的场景❌不推荐
3. STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION（结构化零样本）	✅ 零样本推理
✅ 所有模型通用（含 NVIDIA）
✅ 支持多参数工具（lat+lon）
✅ 结构化 JSON 传参	❌ 无会话记忆（多轮需重复传参）	（你的当前场景）
工具参数：lat+lon（双参数）
提问：“查南康区天气”
Agent 调用：getWeather(lat=25.65, lon=114.77)	你的场景✅最优选择（单轮 + 多参数）
4. CONVERSATIONAL_REACT_DESCRIPTION（带记忆对话）	✅ 继承 STRUCTURED_CHAT 的多参数支持
✅ 内置会话记忆（记住历史信息）
✅ 所有模型通用	❌ 需额外配置记忆组件
❌ 略增加性能开销	（多轮对话场景）
第一轮：“南康区经纬度是多少？”→Agent 记住：25.65/114.77
第二轮：“查这个位置的天气”→直接调用：getWeather(lat=25.65, lon=114.77)	需多轮对话时选择，你的场景✅可选（扩展用）
补充说明（针对你提到的 “OPENAI_MULTI_FUNCTIONS”）
表格
民间俗称	官方对应类型	说明
OPENAI_MULTI_FUNCTIONS	OPENAI_FUNCTIONS	LangChain 无OPENAI_MULTI_FUNCTIONS枚举，OPENAI_FUNCTIONS本身就支持 “同时调用多个函数”（如先查经纬度工具，再查天气工具），是民间对其 “多函数调用能力” 的俗称。