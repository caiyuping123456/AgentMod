import base64
import os

import dotenv
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from sqlalchemy import false

dotenv.load_dotenv()

class FieldInfo(BaseModel):
    path_or_url:str = Field(description="图片的路径或 URL。可以是本地文件路径 (如 'D:/images/chart.png') 或网络图片链接 (如 'http://.../img.jpg')。")
    input_prompt:str = Field(description="你想让模型对这张图片做什么的具体指令。例如：'请提取图中的所有文字'、'详细描述图中的场景'、'这个图表说明了什么趋势？'。指令越具体，回答越准确。")

@tool(
    name_or_callable="image_vision_tool",
    description= "用于分析和理解图片内容的工具。"
                 "当用户需要'看图说话'、'提取图片文字 (OCR)'、'识别图中物体'、'分析图表数据'或'解释截图内容'时调用此工具。"
                 "需要传入图片路径/URL 和具体的分析问题。"
                 "注意：此工具不能生成新图片，只能分析现有图片。"
                 "返回的是对图片的具体描述",
    args_schema=FieldInfo,
    return_direct=False
)
def imageVisionTool(path_or_url:str,input_prompt:str)->str:

    IMAGE_VISION_BASE_URL = os.getenv("IMAGE_VISION_BASE_URL")
    IMAGE_VISION_API_KEY = os.getenv("API_KEY")
    IMAGE_MODEL_NAME = os.getenv("IMAGE_MODEL_NAME")

    image_content_part = {}

    if path_or_url.startswith(("http://", "https://")):
        image_content_part = {
            "type": "image_url",
            "image_url": {"url": path_or_url}
        }
    else:
        if not os.path.exists(path_or_url):
            return f"错误：本地文件不存在 {path_or_url}"

        try:
            with open(path_or_url, "rb") as f:
                image_bytes = f.read()
                base64_str = base64.b64encode(image_bytes).decode("utf-8")

                # 判断文件类型
                ext = os.path.splitext(path_or_url)[1].lower()
                mime_map = {
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".webp": "image/webp",
                    ".gif": "image/gif",
                    ".bmp": "image/bmp",
                    ".tiff": "image/tiff",
                    ".tif": "image/tiff"
                }

                mime_type = mime_map.get(ext)

                data_uri = f"data:{mime_type};base64,{base64_str}"

                image_content_part = {
                    "type": "image_url",
                    "image_url": {"url": data_uri}
                }
        except Exception as e:
            return f"读取本地图片失败：{str(e)}"

    messages = [
        {
            "role": "user",
            "content": [
                image_content_part,
                {"type": "text", "text": input_prompt}
            ]
        }
    ]

    headers = {
        "Authorization": f"Bearer {IMAGE_VISION_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": IMAGE_MODEL_NAME,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.5,
        "top_p": 1.0,
        "stream": False
    }

    try:
        response = requests.post(IMAGE_VISION_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()  # 检查 HTTP 错误

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API 返回异常格式：{result}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP 错误：{e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"请求失败：{str(e)}"
# if __name__ == "__main__":
#     print(imageVisionTool(r"D:\Py_Project\Langcahin\AgentMod\images\img_1772176445_1.jpg","描述一下这个"))
