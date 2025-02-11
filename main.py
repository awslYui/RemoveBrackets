from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import re

"""
！本人完全不懂编程，使用Gemini改写自Removethink插件！
收到消息时，移除消息中的所有全角半角括号及其内容
"""

# 注册插件
@register(name="RemoveBrackets", description="移除消息中的所有全角半角括号及其内容", version="0.1", author="awslYui")
class RemoveBracketsPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        super().__init__(host)  # 必须调用父类的初始化方法

    # 异步初始化
    async def initialize(self):
        pass

    def remove_brackets_content(self, msg: str) -> str:
        """移除消息中的所有全角半角括号及其内容"""

        pattern = r'[（(][\s\S]*?[）)]'  # 匹配全角和半角括号

        result = msg
        iteration = 0
        max_iterations = 10

        while re.search(pattern, result) and iteration < max_iterations:
            result = re.sub(pattern, '', result)
            result = re.sub(r'\n\s*\n', '\n', result.strip()) # 移除多余空行
            iteration += 1

        if iteration >= max_iterations:
            self.ap.logger.warning(f"达到最大迭代次数 {max_iterations}，可能存在异常括号")

        return result

    # 当收到回复消息时触发
    @handler(NormalMessageResponded)
    async def normal_message_responded(self, ctx: EventContext):
        msg = ctx.event.response_text
        if re.search(r'[（(][\s\S]*?[）)]', msg):  # 检查是否存在括号
            processed_msg = self.remove_brackets_content(msg)
            if processed_msg:
                ctx.add_return("reply", [processed_msg])
            else:
                self.ap.logger.warning("处理后的消息为空，跳过回复")

    # 插件卸载时触发
    def __del__(self):
        pass
