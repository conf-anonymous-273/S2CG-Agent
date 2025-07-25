from abc import ABC, abstractmethod
import os
from openai import OpenAI
import dashscope


class LLMInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        根据用户需求生成代码
        :param prompt: 用户需求的文本描述
        :return: 生成的Python代码
        """
        pass


class Qwen_LLM(LLMInterface):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.model = model

    def generate(self, prompt: str) -> str:
        times = 2
        for i in range(times):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {'role': 'system',
                            'content': 'You are a professional Python developer.'},
                        {'role': 'user', 'content': prompt}],
                )
                return completion.choices[0].message.content
            except Exception as e:
                print('API ERROR')
