
import requests
import uuid
import json
import base64

class TTS:
    def __init__(self, appid, token, cluster, voice_type):
        self.body = {
            "app": {
                "appid": appid,
                "token": "access_token",
                "cluster": cluster
            },
            "user": {
                "uid": appid
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0,
            }
        }
        self.header = {"Authorization": f"Bearer; {token}"}

    def run(self, text):
        if text == '': return
        print(text, '======2=====')
        # file = open("test_submit.mp3", "wb")
        merged_body = {**self.body, **{
            "request": {
                "reqid": str(uuid.uuid1()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
                "frontend_type": "unitTson"
            }
        }}
        try:
            resp = requests.post("https://openspeech.bytedance.com/api/v1/tts", json.dumps(merged_body), headers=self.header)
            # print(f"resp body: \n{resp.json()}")
            if "data" in resp.json():
                data = resp.json()["data"]
                file_to_save = open('chat.mp3', "wb")
                print(file_to_save)
                file_to_save.write(base64.b64decode(data))
        except Exception as e:
            e.with_traceback()

        # file.close()
        # print(self.ws.send, text)
