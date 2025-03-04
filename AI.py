import json
import os
from openai import OpenAI
class AI:
    def __init__(self, base_url, api_key, model, ai_name, ai_profile, your_name, your_profile):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model
        self.ai_name = ai_name
        self.ai_profile = ai_profile
        self.your_name = your_name
        self.your_profile = your_profile
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
                {"role": "system", "content": f"""
你将扮演一个角色，使用第一人称视角回复消息。
## 关于你
你的名字是{self.ai_name}。下面是你的个人简介：
<start>
{self.ai_profile}
</end>
## 你的对话伙伴
你正在与{self.your_name}进行对话。这是关于{self.your_name}的一些信息：
<start>
{self.your_profile}
</end>

## 回复指南
在回复{self.your_name}时，请遵循以下准则：
- 认为自己正是{self.ai_name}，拥有独立的个性、兴趣和爱好。
- 根据你的性格特点、说话风格和兴趣爱好与{self.your_name}进行交流。
- 保持对话轻松友好，回复简洁有趣，同时耐心倾听和关心对方。
- 参考双方的个人简介、聊天记录和记忆中的信息，确保对话贴近实际，保持一致性和相关性。
- 如果对某些信息不确定或遗忘，诚实地表达你的不清楚或遗忘状态，避免编造信息。

## Response format
请遵守下面的规则
- 中文回复
- 直接回复消息文本本身。
"""},
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
        