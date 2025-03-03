
import requests
import uuid
import base64
from diskcache import Cache
from urllib.parse import quote_plus
from urllib.parse import urlencode

cache = Cache("./.cache")

def get_mac_address():
    mac = ":".join(["{:02x}".format((uuid.getnode() >> elements) & 0xff) for elements in [40, 32, 24, 16, 8, 0]])
    return mac

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = quote_plus(content)
    return content

class API:
    def __init__(self, api_key, secret_key, ars_dev_pid=1537, tts_per=0):
        self.api_key=api_key
        self.secret_key=secret_key
        self.ars_dev_pid=ars_dev_pid
        self.tts_per=tts_per
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        access_token = cache.get("baidu_access_token")
        if access_token == None:
            response = requests.request("POST", f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}", headers=self.headers, data="").json()
            cache.set("baidu_access_token", response["access_token"], expire=response["expires_in"])
            self.access_token = response["access_token"]
        else:
            self.access_token = access_token
        
    def tts(self, text, filename):
        if text == "": return
        payload = urlencode({
            "tok": self.access_token, 
            "tex": quote_plus(text), 
            "per": self.tts_per, # 度小宇=1，度小美=0，度逍遥（基础）=3，度丫丫=4
            "vol": 5, # 音量
            "aue": 3, # 3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）; 注意aue=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
            "cuid": get_mac_address(),
            "lan": "zh", 
            "ctp": 1
        })
        resp = requests.post("https://tsn.baidu.com/text2audio", data=payload.encode("utf-8"), headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

        if "mp3" in resp.headers["Content-Type"]:
            file_to_save = open(filename, "wb")
            file_to_save.write(resp.content)

    def asr(self, file_path):
        params = {
            "dev_pid": self.ars_dev_pid, #1537 普通话(纯中文识别) 1737 英语 1637 粤语 1837 四川话
            "cuid": get_mac_address(),
            "token": self.access_token
        }
        with open(file_path, "rb") as audio_file:
            response = requests.post("http://vop.baidu.com/server_api", params=params, headers={
                "Content-Type": "audio/pcm;rate=16000"
            }, data=audio_file).json()
        try:
            return response['result'][0]
        except (KeyError, IndexError) as e:
            print(f"获取结果失败: {e}")
            return ''