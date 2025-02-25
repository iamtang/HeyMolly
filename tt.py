from TTS_BAIDU import TTS


tts = TTS()
tts.run('在 Python 中，要实现持久化存储并支持过期时间，可以使用一些常见的库和方法，例如使用 pickle 和 shelve 库，或者通过使用 Redis 等数据库来实现缓存存储。', 'chat.mp3')