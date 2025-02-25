from snowboy import snowboydecoder
import speech_recognition as sr
# import asyncio
from AI import AI
from TTS import TTS
from MusicPlayer import MusicPlayer
# import re
import time
import os
from dotenv import load_dotenv

MODEL_FILE = "heymolly.pmdl"  # 替换为你的模型文件
load_dotenv()

ai = AI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)

tts = TTS(
    appid=os.getenv("APPID"),
    token=os.getenv("TOKEN"),
    cluster=os.getenv("CLUSTER"),
    voice_type=os.getenv("VOICE_TYPE"),
)

# text = ""
# frist=False
mic = sr.Microphone()
recognizer = sr.Recognizer()
# 回调函数，当检测到唤醒词时触发
async def listen_and_transcribe():
    """监听用户语音并转成文本"""
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # 调整噪音水平
        print("请开始说话...")
        try:
            audio_data = recognizer.listen(source, timeout=3)  # 监听语音
            text = recognizer.recognize_google(audio_data, language="zh-CN")  # 语音转文本
            print(f"用户说: {text}")
            ask(text)
        except sr.WaitTimeoutError:
            print("未检测到语音输入")
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError:
            print("语音识别请求失败")

def ask(text):
    # global frist
    # frist=False
    resText = ai.send(text)
    tts.run(resText)
    # while frist == False:
    #     await asyncio.sleep(1)
    player = MusicPlayer('reply.mp3')
    player.play()
    while True:
        time.sleep(1)
        if player.is_finished():
            print('====finished==')
            break

# def callback(t, file, isEnd):
#     global text, frist
#     text += t or ""
#     if('。' in text):
#         match = re.search(r'([^。]+[。])(.*)', text)
#         if(match != None):
#             tts.run(match.group(1), file)
#             frist = True
#             text = match.group(2)
#     elif isEnd:
#         tts.run(text, file)
#         frist = True

def main():
    # 初始化 Snowboy 检测器
    detector = snowboydecoder.HotwordDetector(MODEL_FILE, sensitivity=0.5)
    print("开始监听唤醒词...")
    player = MusicPlayer('zai.mp3')
    player.play()
    # 开始监听
    detector.start(listen_and_transcribe, sleep_time=0.03)  # 设置检测间隔
    # 停止监听
    detector.terminate()


if __name__ == '__main__':
    ask('你是谁')