import requests

class Sol():
    """
    Sol 类用于与 Solana 区块链交互，获取账户信息、代币信息和交易历史。
    """
# {'http': 'http://127.0.0.1:7897','https': 'http://127.0.0.1:7897'}
    def __init__(self, address="", proxies={}):
        self.urls = {
            "SOL": "https://api-v2.solscan.io/v2/account",
            "Token": "https://api-v2.solscan.io/v2/account/tokens",
            "history": "https://api-v2.solscan.io/v2/account/transaction",
        }
        self.headers = {
            "origin": "https://solscan.io",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        self.address = address
        self.proxies = proxies
        self.session = requests.Session()

    def get_res(self, url):
        """
        获取指定 URL 的响应数据。

        :param url: 请求的 URL。
        :return: JSON 格式的响应数据，如果请求失败则返回 None。
        """
        params = {
            "address": self.address
        }
        
        try: 
            res = requests.get(url=url, params=params, headers=self.headers, proxies=self.proxies)
            # print(res)
            if res.status_code == 200:
                return res.json()
            else:
                # print("请求失败")
                raise ValueError("请求被拒绝了")
        except:
            # print("请求失败")
            raise ValueError("请求失败")
            # return None
        
    def get_SOL(self, url):
        """
        获取账户的 SOL 余额。

        :param url: 请求的 URL。
        :return: 包含账户余额的字典。
        """
        res = self.get_res(url)
        # print(res)
        SOL = res["data"]  # type: ignore
        balance = SOL["lamports"]
        account = {
            "余额": balance / 1000000000,
        }
        return account
    
    def get_Token(self, url):
        """
        获取账户持有的代币信息。

        :param url: 请求的 URL。
        :return: 包含代币数量和当前持有代币的字典。
        """
        res = self.get_res(url)
        Tokens = res["data"]  # type: ignore
        count = Tokens["count"]
        props = Tokens["tokens"]
        token = {
            "数量": count,
            "当前持有": props
        }
        return token
    
    def get_Transaction(self, url):
        """
        获取账户的交易历史。

        :param url: 请求的 URL。
        :return: 包含交易信息的字典列表。
        """
        res = self.get_res(url)
        transactions = [{
            "time": i["blockTime"],
            "by": i["signer"],
            "value": i["sol_value"],
            "fee": i["fee"],
        } for i in res["data"]["transactions"]]
        return transactions
    

    def get_Overview(self):
        """
        获取账户的概览信息，包括 SOL 余额和代币信息。

        :return: 包含账户和代币信息的字典。
        """
        account = self.get_SOL(self.urls["SOL"])
        token = self.get_Token(self.urls["Token"])
        return {"account": account, "token": token}

    def get_History(self):
        """
        获取账户的交易历史。

        :return: 包含交易历史的字典。
        """
        transaction = self.get_Transaction(self.urls["history"])
        return {"transaction": transaction}
        
    def get_sol_range(self, start, end):
        """
        获取指定范围内的 SOL 数据。

        :param start: 起始值。
        :param end: 结束值。
        :return: JSON 格式的响应数据。
        """
        return self.session.get(self.url + f'/api/v2/sol/{start}/{end}').json()
    
    def main(self):
        """
        主方法，用于获取账户概览和交易历史。

        :return: 包含账户概览和交易历史的字典。
        """
        overview = self.get_Overview()
        history = self.get_History()
        return {"overview": overview, "history": history}
    
if __name__ == "__main__":
    sol = Sol("7nyhQzUMjcj7fEnG5WqMbTbC8e3Z5m6fub2NDAu7E2Nz", proxies={'http': 'http://127.0.0.1:7897','https': 'http://127.0.0.1:7897'})
    # print(sol.main())
    data = sol.main()
    import json
    data = json.dumps(data)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(str(data))