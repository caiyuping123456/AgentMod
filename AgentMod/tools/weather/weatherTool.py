import datetime
import os

import dotenv
from pydantic import BaseModel, Field

import requests
from langchain_core.tools import tool

from AgentMod.utils import weatherCode as weather

dotenv.load_dotenv()

class FieldInfo(BaseModel):
    latitude: float = Field(description="查询地点的纬度，浮点型（如南康区25.65）")
    longitude: float = Field(description="查询地点的经度，浮点型（如南康区114.77）")

## latitude:纬度
## longitude：经度
# latitude:int,longitude:int
## return_direct表示是否直接提交给调用方
@tool(name_or_callable="search_current_weather",
      description="查询指定经纬度的**当天实时天气**（温度℃、风速m/s、风向、天气状况）。【重要限制】"
                  "1. 仅能查询当前实时天气。本工具返回的是气象局的最新观测数据。即使返回数据中的年份/日期与系统当前时间看似不一致（如因时区或数据源延迟），"
                  "只要数据是最新的，就视为有效，请直接报告给用户，不要因为年份差异而拒绝回答或编造“无法查询”的理由。如果用户明确询问“明年”或“过去某年”的历史天气，才回复无法查询。"
                  "2. 输出必须为**中文**。"
                  "3. 返回结果需包含：气温、风速、风向（如：正南 180°）、天气状况及数据更新时间。",
      args_schema=FieldInfo,## 使用参数校验模型
      return_direct=False)
def getWeather(latitude:float,longitude:float)->str:
    #这个是获取天气请求的url
    url = os.getenv("WEATHER_TOOL_BASE_URL")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True, ##获取当前的天气
        "models": "cma_grapes_global",
    }
    try:
        re = requests.get(url, params=params)
        ## 获取json
        current_weather = re.json().get("current_weather")

        temp = current_weather["temperature"]  # 气温
        wind_speed = current_weather["windspeed"]  # 风速
        wind_dir = current_weather["winddirection"]  # 风向
        weather_code = current_weather["weathercode"]  # 天气代码
        is_day = True if current_weather["is_day"] == 1 else False  # 是否白天
        weather_time = current_weather["time"] # 天气时间
        readable_time = "未知"
        if weather_time:
            try:
                # 解析 ISO 时间
                dt = datetime.fromisoformat(weather_time.replace('Z', '+00:00'))
                # 格式化为：月 - 日 HH:MM (忽略年份，减少 LLM 对年份的敏感度，或者保留年份但确保时区正确)
                # 如果必须保留年份，请确保你的系统时间正确
                readable_time = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                readable_time = weather_time
        weather_condition = weather.get_weather_desc(weather_code)

        return (f"纬度{latitude}，经度{longitude}，查询到的今天的气温是：{temp}，风速是：{wind_speed}，风向是：{wind_dir},"
                f"天气情况是：{weather_condition}，是否是白天：{is_day}，数据时间：{readable_time}")
    except Exception as e:
        return f"天气查询失败：{str(e)}"
