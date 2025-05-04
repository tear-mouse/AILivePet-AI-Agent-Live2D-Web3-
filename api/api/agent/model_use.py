import requests
import json

class model_use:
    def __init__(self, bot_id, api_token, max_chat_rounds=20, stream=True, history=None):
        """
        初始化 Coze 类的实例。

        :param bot_id: 您的 Coze 机器人 ID。
        :param api_token: 用于认证的 API 令牌。
        :param max_chat_rounds: 保存的最大对话轮数。
        :param stream: 是否使用流式响应。
        :param history: 初始的对话历史记录。
        """
        self.bot_id = bot_id
        self.api_token = api_token
        self.history = history if history is not None else []
        self.max_chat_rounds = max_chat_rounds
        self.stream = stream
        self.url = 'https://api.coze.cn/open_api/v2/chat'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'api.coze.cn',
            'Connection': 'keep-alive'
        }

    def build_messages(self):
        """
        构建对话历史记录的消息格式。

        :return: 格式化的消息列表。
        """
        messages = []
        for prompt, response in self.history:
            messages.append({"role": "user", "content": prompt, "content_type": "text"})
            messages.append({"role": "assistant", "content": response})
        return messages

    def chat(self, query):
        """
        发送用户查询并获取响应。

        :param query: 用户的输入文本。
        :return: 机器人返回的响应文本。
        """
        data = {
            "conversation_id": "123",  # 可以根据需要生成唯一的 conversation_id
            "bot_id": self.bot_id,
            "user": "user",  # 可以根据需要自定义用户标识
            "query": query,
            "stream": self.stream,
            "chat_history": self.build_messages()
        }
        response = requests.post(self.url, headers=self.headers, json=data, stream=self.stream)

        if response.status_code == 200:
            if self.stream:
                return self._handle_stream_response(response)
            else:
                return self._handle_non_stream_response(response)
        else:
            raise Exception(f"请求失败，状态码：{response.status_code}")

    def _handle_non_stream_response(self, response):
        """
        处理非流式响应。

        :param response: HTTP 响应对象。
        :return: 解析后的响应文本。
        """
        dic = response.json()
        messages = dic.get('messages', [])
        return self._extract_response(messages)

    def _handle_stream_response(self, response):
        """
        处理流式响应。

        :param response: HTTP 响应对象。
        :return: 解析后的响应文本。
        """
        messages = []
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    line = line[5:]
                dic = json.loads(line)
                if dic.get('event') == 'message':
                    messages.append(dic['message'])
        return self._extract_response(messages)

    def _extract_response(self, messages):
        """
        从消息列表中提取机器人响应。

        :param messages: 消息列表。
        :return: 机器人响应的文本内容。
        """
        response_content = []
        for message in messages:
            if message.get('type') == 'answer':
                response_content.append(message.get('content', ''))
        return ''.join(response_content)

    def __call__(self, query):
        """
        使实例对象可调用，发送查询并更新对话历史。

        :param query: 用户的输入文本。
        :return: 机器人返回的响应文本。
        """
        if len(self.history) >= self.max_chat_rounds:
            self.history = self.history[-self.max_chat_rounds:]
        response = self.chat(query)
        self.history.append((query, response))
        return response




