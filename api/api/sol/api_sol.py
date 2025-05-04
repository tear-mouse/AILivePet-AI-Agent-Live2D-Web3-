from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.sol.fetch import Sol
router = APIRouter()

@router.get("/sol")
async def sol(address: str | None = "", proxies: dict | None = None):
    print(address)
    if address:
        sol = Sol(address, proxies=proxies)
    else:
        sol = Sol()
        # return {"message": "address is None"}
    res = sol.main()
    content = {"message": res}
    return JSONResponse(
        content=content,
        media_type="application/json; charset=utf-8"
    )