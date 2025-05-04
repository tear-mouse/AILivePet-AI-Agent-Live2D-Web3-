1. requirements.txt
    ```ini
    fastapi
    "uvicorn[standard]"
    requests
    ```

2. 安装依赖

    ```bash
    pip install -r requirements.txt
    ```

3. 当然, 你也可以使用虚拟环境

    - for `Windows`
        ```bash
        python3 -m venv venv
        venv/bin/activate
        pip install -r requirements.txt
        ```

    - for `Unix`
    
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```
    
3. 运行服务
    - 调试
        ```bash
        uvicorn main:app --reload
        ```
    - 使用
    
        ```
        uvicorn main:app
        ```
    
        
    

