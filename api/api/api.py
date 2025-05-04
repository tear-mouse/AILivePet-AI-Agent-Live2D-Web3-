from fastapi import APIRouter
import time
from api.sol.api_sol import router
from api.agent.api_agent import router_agent
api_router = APIRouter()
api_router.include_router(router, prefix="")
api_router.include_router(router_agent, prefix="")

@api_router.get("/ping")
def ping():
    return {"message": time.time()}