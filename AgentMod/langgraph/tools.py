from AgentMod.tools.toos_map import ToolIocContainer


## 放回工具
def getTools():
    tool_path = r"D:\Py_Project\Langcahin\AgentMod\tools\tool_config.yaml"
    ToolIocContainer.load_tool_config(tool_path)
    return ToolIocContainer.get_tool()