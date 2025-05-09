'''
注意使用要以utils/的父目录作为项目的根目录

目前提供函数: sol
>>> from utils.fetch import sol
>>> sol(address:str) -> dict

'''
# import sys
# import os
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)
from modules.chain_info import *

def sol(address:str) -> dict:
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
    try:
        return {"success": True, "data": Sol(address).main()}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
