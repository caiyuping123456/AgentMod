import os

import dotenv
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

dotenv.load_dotenv()

class FieldInfo(BaseModel):
    query:str = Field(description="搜索关键词或查询语句。用于在互联网上检索最新的信息、新闻、事实或数据。请确保关键词具体明确。")

# 联网search
@tool(name_or_callable="web_search",
      description= "用于搜索互联网上的最新信息、实时新闻、突发事件或验证未知事实。当用户询问的内容涉及当前时间、最新数据、具体人物/事件的最新动态，或者你的内部知识库无法确认时，**必须**调用此工具。严禁使用过时的内部知识瞎编，一切以搜索结果为准。输入参数为搜索关键词。",
      args_schema=FieldInfo,
      return_direct=False)
def webSearch(query:str)->str:
    webSearchUrl = os.getenv("WEB_SEARCH_BASE_URL")
    params = {
        "q" : query,
        "format": "json",
    }
    try:
        re = requests.get(url=webSearchUrl, params=params)
        # 获取json
        jsonString = re.json()
        ans = "正常查找，但是未查询到任何数据"
        results = jsonString["results"]
        if len(results) != 0:
            index = 1
            for result in results:
                # 标题
                title = result["title"]
                # 内容
                content = result["content"]
                item = f"{index}.【{title}】\n   内容：{content}"
                ans += item+"\n"
                index +=1

            return ans
        else:
            return ans
    except Exception as e:
        return "出现未知异常，未查询到任何数据"+e

