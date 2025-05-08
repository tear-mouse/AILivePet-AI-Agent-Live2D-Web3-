from dotenv import load_dotenv
from pathlib import Path
import os
from model_use import model_use
import random

# 正确加载 .env 文件
load_dotenv(dotenv_path=Path('.') / '.env')

# 从环境变量中获取 bot_id 和 token
bot_id = os.getenv("cat_bot_id")
api_token = os.getenv("api_token")

# 初始化 Coze Chat 对象
coze_chat = model_use(bot_id=bot_id, api_token=api_token)

def get_ai_cat_reply(user_input):
    try:
        # 调用 Coze Chat 模型获取对话回复
        response = coze_chat(user_input)
        return response
    except Exception as e:
        # 处理可能的错误并返回错误信息
        return f"喵呜，好像出错了：{e}"

def random_cat_phrase():
    phrases = [
        "哼，你终于来看我了~",
        "我才没有在等你呢，真的没有喵！",
        "陪我玩嘛，不然我生气了哦！",
        "要抱抱...现在！",
        "再摸我脑袋我就要咬你了喵！（其实不会啦~）",
        "今天也要加油哦，但别忘了休息~",
        "嘿嘿，偷偷告诉你，其实我很喜欢你呢~",
    ]
    prefix = random.choice(["嗷呜~", "哎呀~", "喵嗷~", "嘿嘿~", "哼哼~"])
    return f"{prefix} {random.choice(phrases)}"

def on_click(self, event):
        msg = random_cat_phrase()
        self.text_box.setText(msg)
