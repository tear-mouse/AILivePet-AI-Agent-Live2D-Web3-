'''
注意使用要以root(root/utils/fetch.py)作为项目的根目录
'''
from api.sol.fetch import Sol

def fetch_sol(address:str) -> dict:
    """
    获取某个 Sol 地址的概览与交易历史
    
    Parameters
    ----------
    address : str
        要查询的 Sol 地址 

    Returns
    -------
    dict
        返回如下结构：
        {
            "overview": ...,  # 地址概况数据
            "history": ...    # 历史交易数据
        }
        
    Examples
    --------
    >>> from utils.fetch import getsol
    >>> result = getsol("")
    >>> print(result["overview"])
    >>> print(result["history"])
    """
    return Sol(address).main()
    
    