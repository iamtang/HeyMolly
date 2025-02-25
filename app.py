import asyncio
import struct
import pvporcupine
import pyaudio
import speech_recognition as sr
import re
from dotenv import load_dotenv
import os
from AI import AI
from TTS import TTS
from MusicPlayer import MusicPlayer

load_dotenv()
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

appid = os.getenv("APPID")
token = os.getenv("TOKEN")
cluster = os.getenv("CLUSTER")
voice_type = os.getenv("VOICE_TYPE")

ai = AI(
    base_url=base_url,
    api_key=api_key,
    model=model # ep-20250219163101-p5zk6
)

tts = TTS(
    appid=appid,
    token=token,
    cluster=cluster,
    voice_type=voice_type,
)

text = ""
frist=False
# 初始化语音识别
recognizer = sr.Recognizer()
mic = sr.Microphone()
# 初始化 Porcupine 唤醒词检测
porcupine = pvporcupine.create(
    access_key="XcEt9naMKyhAYoKbNr6eJyRI8wqSX0VWkQ0/r7xGp6QAP42BMWqi0Q==",
    keyword_paths=["./hey-molly_en_mac_v3_0_0.ppn"]
)

# 初始化麦克风音频流
audio = pyaudio.PyAudio()
voice_stream = audio.open(
    input_device_index=0,
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)
async def callback(file, t, isEnd):
    global text, frist
    text += t
    if('。' in text):
        match = re.search(r'([^。]+[。])(.*)', text)
        if(match != None):
            await tts.run(match.group(1), file)
            frist = True
            text = match.group(2)
    elif isEnd:
        await tts.run(text, file)
        frist = True

async def listen_and_transcribe():
    """监听用户语音并转成文本"""
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # 调整噪音水平
        print("请开始说话...")
        try:
            audio_data = recognizer.listen(source, timeout=3,)  # 监听语音
            text = recognizer.snowboy_wait_for_hot_word(audio_data, language="zh-CN")  # 语音转文本
            print(f"用户说: {text}")
            await say(text)
        except sr.WaitTimeoutError:
            print("未检测到语音输入")
        except sr.UnknownValueError:
            print("无法识别语音")
        except sr.RequestError:
            print("语音识别请求失败")

async def say(text):
    global frist
    frist=False
    await tts.connect()
    asyncio.create_task(ai.send(text, callback))
    while frist == False:
        await asyncio.sleep(1)
    player = MusicPlayer('chat.mp3')
    player.play()
    while True:
        await asyncio.sleep(1)
        if player.is_finished():
            print('====finished==')
            break

async def main():
    while True:
        print("正在监听唤醒词...")
        audio_data = voice_stream.read(porcupine.frame_length, exception_on_overflow=False)
        audio_data_unpacked = struct.unpack_from("h" * porcupine.frame_length, audio_data)
        
        # 处理唤醒词
        keyword_index = porcupine.process(audio_data_unpacked)
        if keyword_index >= 0:
            player = MusicPlayer('zai.mp3')
            player.play()
            await listen_and_transcribe()  # 监听用户语音

if __name__ == '__main__':
    asyncio.run(main())
    # 停止唤醒词检测
    # porcupine.delete()
    # voice_stream.close()
    # audio.terminate()