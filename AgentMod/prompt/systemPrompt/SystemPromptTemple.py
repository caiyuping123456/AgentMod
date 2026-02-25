import os

from langchain_core.prompts import SystemMessagePromptTemplate
from AgentMod.utils import ymlUtils as yml


# 读取文件，获取系统提示词
def getSystemPromptTemplate()->SystemMessagePromptTemplate:
    path = r"D:\Py_Project\Langcahin\AgentMod\prompt\prompt.yml"
    result = yml.read_yml(path)
    temple = "根据实际情况回答"
    if not result is None:
        if not result["system_prompt"] is None:
            temple = result["system_prompt"]["temple"]
    return SystemMessagePromptTemplate.from_template(
        template=temple
    )