from dotenv import load_dotenv
from pathlib import Path
import os
from model_use import model_use
import random

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path=Path('.') / '.env')

#  bot_id 和 token
bot_id = os.getenv("fox_bot_id")  
api_token = os.getenv("api_token")
print({api_token})
print({bot_id})
# 初始化Agent
coze_chat = model_use(bot_id=bot_id, api_token=api_token)

print("狐宝已现身 ✧(≖ ◡ ≖✿) 有什么心事想和我说说？")

def get_ai_fox_reply(user_input: str)-> str:
    user_input = user_input.strip()
    
    if user_input.lower()in ['exit','quit']:
        return "狐宝隐入迷雾中，静待你的召唤~ (^_−)−☆ 晚安~"
    
    if not user_input:
        return "欸?你没说话，狐宝的小耳朵都竖起来听了呢~"
    
    try:
        response = coze_chat(user_input)
        print(response)
    except Exception as e:
        print("呜呜...狐宝的灵力有点紊乱了，似乎出错了：", e)


def random_fox_phrase():
    phrases = [
        "你怎么现在才来找狐宝~哼~",
 	    "狐宝已经在等你啦~",	
        "抱一下可以续灵力30分钟 (^_−)−☆",	
        "别一直点我啦，会害羞的>///<",	
	    "我不是小狐狸，我是超可爱的狐宝哒~",	
	    "今天也是美好的一天呢，一起加油!",	
        "累了吗?来，狐宝给你抱抱~",	
	    "狐宝的灵力好充沛，快来玩!"
    ]
    return f"{random.choice(phrases)}"
