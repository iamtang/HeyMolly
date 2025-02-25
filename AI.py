import json
import os
from openai import OpenAI

class AI:
    def __init__(self, base_url, api_key, model):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model
        self.history_path = os.path.join(os.path.dirname(__file__), "history.json")
        
    # 读取聊天历史
    def get_chat_history(self):
        if not os.path.exists(self.history_path):
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump({"list": []}, f, ensure_ascii=False)
        
        with open(self.history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        
        return history["list"]

    # 保存聊天历史
    def save_chat_history(self, chat_history):
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump({"list": chat_history}, f, ensure_ascii=False)

    # 清空聊天历史
    def delete_chat_history(self):
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump({"list": []}, f, ensure_ascii=False)

    def send(self, content):
        chat_history = self.get_chat_history()
        chat_history.append({"role": "user", "content": content})
        stream = self.client.chat.completions.create(
            model=self.model,
            stream=True,
            messages=[
                {"role": "system", "content": "你是一名全无所不知的老师，要实事求是，不能虚构作答，你叫Molly，通熟易懂地解答用户的提问，不需要换行和空格"},
                *chat_history
            ]
        )
        text = ""
        for chunk in stream:
            if not chunk.choices:
                continue
            text += chunk.choices[0].delta.content or ''
            
            # await callback(chunk.choices[0].delta.content, file, False)
        # await callback('', file, True)
        chat_history.append({"role": "assistant", "content": text})
        self.save_chat_history(chat_history)
        return text
        