from snowboy import snowboydecoder
import speech_recognition as sr
# import asyncio
from AI import AI
from BAIDU_API import API
from MusicPlayer import MusicPlayer
# import re
import time
import os
from dotenv import load_dotenv

MODEL_FILE = "assets/heymolly.pmdl"  # 替换为你的模型文件
load_dotenv()

ai = AI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)
api = API(
    api_key=os.getenv("BAIDU_API_KEY"),
    secret_key=os.getenv("BAIDU_SECRET_KEY")
)
# tts = TTS(
#     appid=os.getenv("APPID"),
#     token=os.getenv("TOKEN"),
#     cluster=os.getenv("CLUSTER"),
#     voice_type=os.getenv("VOICE_TYPE"),
# )
# text = ""
# frist=False
mic = sr.Microphone()
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
def rmFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"{file_path} 不存在")
# 回调函数，当检测到唤醒词时触发
def listen_and_transcribe():
    ai.delete_chat_history()
    """监听用户语音并转成文本"""
    player = MusicPlayer('assets/zai.mp3')
    player.play()
    with mic as source:
        while 1:
            path = 'audio/chat.pcm'
            recognizer.adjust_for_ambient_noise(source, duration=1)  # 调整噪音水平
            recognizer.energy_threshold *= 1.5
            print("请说话...")
            try:
                start_time = time.time()
                audio_data = recognizer.listen(source, timeout=3)  # 监听语音
                end_time = time.time()
                print(end_time - start_time)
                wav_data = audio_data.get_wav_data()  # 获取 WAV 格式的二进制数据
                
                # 去除 WAV 头部，只保留 PCM 数据
                pcm_data = wav_data[44:]  # 前 44 字节是 WAV 头部，去掉它
                # 将 PCM 数据保存到文件
                with open(path, "wb") as f:
                    f.write(pcm_data)

                print("音频已保存为 " + path)
                text = api.asr(path)
                # rmFile(path)
                print(f"用户说: {text}")
                if text == '':
                    break
                break
                ask(text)
            except sr.WaitTimeoutError:
                print("未检测到语音输入")
                break
            except sr.UnknownValueError:
                print("无法识别语音")
                break
            except sr.RequestError:
                print("语音识别请求失败")
                break

def ask(text):
    # global frist
    # frist=False
    filename = 'audio/reply.mp3'
    resText = ai.send(text)
    print(f"AI说: {resText}")
    api.tts(resText, filename)
    # while frist == False:
    #     await asyncio.sleep(1)
    player = MusicPlayer(filename)
    player.play()
    while True:
        time.sleep(1)
        if player.is_finished():
            print('====finished==')
            break
    # 清空记录
    rmFile(filename)


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
    # 开始监听
    detector.start(listen_and_transcribe, sleep_time=0.03)  # 设置检测间隔
    # 停止监听
    detector.terminate()


if __name__ == '__main__':
    # api.asr("output.pcm")
    listen_and_transcribe()