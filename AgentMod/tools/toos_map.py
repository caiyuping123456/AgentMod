# ioc_container.py
import importlib
import yaml
from langchain_core.tools import Tool, BaseTool
from AgentMod.utils import logging as log


class ToolIocContainer:
    """静态IOC容器类：无需实例化，直接通过类调用方法"""
    loaded_functions = []  # 列表缓存：[(tool_name, func), ...]
    tool_config = None  # 配置缓存

    @classmethod
    def load_tool_config(cls, config_path: str):
        """加载工具配置（类方法，直接通过类调用）"""
        if cls.tool_config is None:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cls.tool_config = yaml.safe_load(f)
                log.info(f"配置加载成功：{cls.tool_config}")
                log.info("开始进行初始化所有tool工具")
                cls._init_tools()
            except FileNotFoundError:
                raise RuntimeError(f"配置文件不存在：{config_path}")
            except yaml.YAMLError:
                raise RuntimeError(f"配置文件格式错误：{config_path}")
        return cls.tool_config

    @classmethod
    def _init_tools(cls):
        """获取到tools"""
        if cls.tool_config is None:
            cls.tool_config = ToolIocContainer.load_tool_config()
        tools = cls.tool_config["tools"]
        for tool_name, config in tools.items():
            # config 现在是字典：{'module': '...', 'function': '...', ...}
            # 安全获取字段
            module_name = config.get("module", "")
            func_name = config.get("function", "")
            description = config.get("description", f"工具 {tool_name}，无描述")

            # 校验
            if not module_name or not func_name:
                log.warning(f"跳过无效配置 [{tool_name}]: module或function为空")
                continue

            log.info(f"正在加载工具：[{tool_name}] -> 模块={module_name}, 方法={func_name}")

            try:
                full_module_path = module_name

                module = importlib.import_module(full_module_path)

                if hasattr(module, func_name):
                    func_obj = getattr(module, func_name)

                elif hasattr(module, module_name.split('.')[-1]):  # 尝试获取同名类
                    class_name = module_name.split('.')[-1]
                    target_class = getattr(module, class_name)
                    if hasattr(target_class, func_name):
                        func_obj = getattr(target_class, func_name)
                    else:
                        instance = target_class()
                        func_obj = getattr(instance, func_name)
                else:
                    log.error(f"在模块 {full_module_path} 中找不到 {func_name} 或类 {module_name}")
                    continue

                final_tool = None
                if isinstance(func_obj, BaseTool):
                    log.info(f"检测到 {func_name} 已是 Tool 对象，添加")
                    final_tool = func_obj
                elif callable(func_obj):
                    log.info(f"检测到 {func_name} 是普通函数，封装为 Tool")
                    final_tool = Tool(
                        name=tool_name,
                        func=func_obj,
                        description=description
                    )

                else:
                    log.error(f"{func_name} 既不是 Tool 对象也不是可调用函数，类型为：{type(func_obj)}")
                    continue

                # 加入列表
                cls.loaded_functions.append(final_tool)
                log.info(f"成功注册 LangChain Tool: {tool_name}")

            except ModuleNotFoundError:
                log.error(f"找不到模块：{full_module_path} (请检查路径是否正确，是否需要加包名前缀)")
            except Exception as e:
                log.error(f"加载工具 [{tool_name}] 时发生异常：{e}", exc_info=True)

    @classmethod
    def get_tool(cls):
        return cls.loaded_functions

# 测试：静态类调用示例（无需实例化）
if __name__ == "__main__":

    # 第一步：加载配置（直接通过类调用）
    ToolIocContainer.load_tool_config("tool_config.yaml")
    print(ToolIocContainer.loaded_functions)
    # 第二步：第一次调用（列表为空，加载并添加）
    print("\n===== 第一次调用 =====")
    result1 = ToolIocContainer.call_tool("web_search", query="开心")

    # 第三步：第二次调用（复用缓存）
    print("\n===== 第二次调用 =====")
    result2 = ToolIocContainer.call_tool("web_search", query="快乐")

    # 查看静态变量状态
    print(f"\n📊 最终列表状态：{ToolIocContainer.loaded_functions}")