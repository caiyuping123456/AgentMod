import base64
import json
import logging
import os
import time
from typing import Any

import dotenv
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

dotenv.load_dotenv()

class FieldInfo(BaseModel):
    prompt:str = Field(description="这个是图片生成工具的提示词参数")


@tool(name_or_callable="image_generation",
      description="用于根据文字描述生成高质量图像的工具。"
                  "当用户请求'画一张图'、'生成图片'、'展示...的样子'、'创作插图'或需要将抽象概念可视化时使用此工具。"
                  "输入必须包含对主体、背景、风格、光照和颜色的详细描述。"
                  "如果用户描述模糊，请先追问细节再生成，或尝试基于常识补充细节后生成。"
                  "返回的是生成图片的保存目录",
      args_schema=FieldInfo,
      return_direct=False)
def imageGeneration(prompt:str)-> list[Any]:
    url = os.getenv("IMAGE_BASEURL")
    api_key = os.getenv("IMAGE_API_KEY")
    model_name = os.getenv("IMAGE_MODEL")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8"
    }

    payload = {
        "model": model_name,
        "prompt": prompt,
        "image_size": "1024x1024",
        "batch_size": 1,
        "num_inference_steps": 20,
        "guidance_scale": 7.5
    }

    save_dir = r"D:\Py_Project\Langcahin\AgentMod\images"
    if save_dir is None:
        save_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(save_dir, exist_ok=True)

    logging.info(f"开始调用 SiliconFlow API 生成图片...")
    response = requests.post(
        url=url,
        headers=headers,
        json=payload,
        timeout=60,
        verify=False
    )
    response.raise_for_status()

    response.encoding = "utf-8"
    result = json.loads(response.text)
    saved_paths = []
    timestamp = int(time.time())

    # 兼容多种响应结构
    img_datas = result.get("data", []) or result.get("images", []) or []
    if not img_datas and isinstance(result, list):
        img_datas = result
    result = ""
    err = ""

    for idx, img_data in enumerate(img_datas):
        # 兼容不同的 Base64 字段名
        img_base64 = img_data.get("b64_json") or img_data.get("base64") or img_data.get("image")

        if img_base64:
            # 解码并保存图片
            try:
                img_bytes = base64.b64decode(img_base64)
                filename = f"img_{timestamp}_{idx + 1}.jpg"
                save_path = os.path.join(save_dir, filename)

                with open(save_path, "wb") as f:
                    f.write(img_bytes)

                saved_paths.append(save_path)
                result +=save_path
                logging.info(f"第 {idx + 1} 张图片保存成功：{save_path}")
            except base64.binascii.Error:
                logging.error(f"第 {idx + 1} 张图片 Base64 解码失败，跳过")
                err += f"第 {idx + 1} 张图片 Base64 解码失败，跳过"
        else:
            # 尝试 URL 方式（部分模型返回 URL 而非 Base64）
            img_url = img_data.get("url")
            if img_url:
                try:
                    img_resp = requests.get(img_url, timeout=30, verify=False)
                    img_resp.raise_for_status()
                    filename = f"img_{timestamp}_{idx + 1}.jpg"
                    save_path = os.path.join(save_dir, filename)
                    with open(save_path, "wb") as f:
                        f.write(img_resp.content)
                    saved_paths.append(save_path)
                    result += save_path
                    logging.info(f"第 {idx + 1} 张图片（URL 下载）保存成功：{save_path}")
                except Exception as e:
                    logging.error(f"第 {idx + 1} 张图片 URL 下载失败：{str(e)}")
                    err += f"第 {idx + 1} 张图片 URL 下载失败：{str(e)}"
            else:
                print(
                    f"第 {idx + 1} 张图片无 Base64/URL 数据，字段：{list(img_data.keys()) if isinstance(img_data, dict) else '非字典'}")
                err = f"第 {idx + 1} 张图片无 Base64/URL 数据，字段：{list(img_data.keys()) if isinstance(img_data, dict) else '非字典'}"

    if len(saved_paths) == 0:
        return err
    return result