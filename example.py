from utils import fetch

res = fetch.sol("7nyhQzUMjcj7fEnG5WqMbTbC8e3Z5m6fub2NDAu7E2Nz")
res = fetch.sol("7nyhQzUMjcj7fEnG5WqMbTbC8e3Z5m6fub2NDAu7E2Nz", port="7890") # 使用代理

# if res["success"]:
#     print(res["data"])
# else:
#     print(f"Error: {res['error']}")
    
data = res["data"] if res.get("success") else f"Error: {res.get('error')}"
print(data)