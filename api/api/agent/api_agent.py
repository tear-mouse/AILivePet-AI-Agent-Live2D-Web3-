from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.agent import cat

router_agent = APIRouter()

@router_agent.get("/agent_cat")
async def agent_cat(user_input: str | None = ""):
    return {cat.random_cat_phrase():cat.get_ai_reply(user_input)} if user_input else cat.random_cat_phrase()

# @router_agent.get("/agent_fox")
# async def agent_cat(user_input: str | None = ""):
#     return fox.get_ai_reply(user_input)