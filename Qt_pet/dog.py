from dotenv import load_dotenv
from pathlib import Path
import os
from model_use import model_use
import random



# 正确加载 .env 文件
load_dotenv(dotenv_path=Path('.') / '.env')

# 从环境变量中获取 bot_id 和 token
bot_id = os.getenv("dog_bot_id")
api_token = os.getenv("api_token")

# 初始化 Coze Chat 对象
coze_chat = model_use(bot_id=bot_id, api_token=api_token)

print("小旺上线啦~ 有什么想对我说的？(输入 'exit' 退出聊天)\n")

def get_ai_dog_reply(user_input: str) -> str:
    user_input = user_input.strip()

    if user_input.lower() in ['exit', 'quit']:
        return "汪~ 那我回狗窝打个呼噜咯，记得好好休息，晚安~ 🐾"

    if not user_input:
        return "汪？你说什么呢，我没听清~"

    try:
        response = coze_chat(user_input)
        return f"{response}"
    except Exception as e:
        return f"呜呜...狗狗脑袋转不过来了，好像出错了：{e}"


def random_dog_phrase():
    phrases = [
        "汪！今天也要开心哦~",
            "主人在干嘛呢？我在想你了~",
            "来摸摸我的头嘛~",
            "陪我玩一会儿嘛~汪！",
            "记得喝水水哦~",
            "要不要我给你讲个笑话？汪！",
            "嘿嘿，偷偷告诉你，我是最聪明的小狗！"
    ]
    return f" {random.choice(phrases)}"
