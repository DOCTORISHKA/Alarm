import time
from mss import mss
import pyaudio
import wave
import keyboard


audio_file = wave.open("sample.wav")
FORMAT = audio_file.getsampwidth() # глубина звука
CHANNELS = audio_file.getnchannels() # количество каналов
RATE = audio_file.getframerate() # частота дискретизации
N_FRAMES = audio_file.getnframes() # кол-во отсчетов
audio = pyaudio.PyAudio()
endBtn = ''
startBtn = ''
timer = 0.0


while(True):
    if(keyboard.is_pressed('alt')):
        mss().shot()
        while(timer <= 60.0):
            time.sleep(1)
            timer += 1
            print(timer)
            if(keyboard.is_pressed('pause')):
                timer = 0.0
                break
            elif(keyboard.is_pressed('end')):
                break
            if timer == 60.0:
                out_stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True)
                out_stream.write(audio_file.readframes(N_FRAMES))  # отправляем на динамик
                timer = 0.0
                break
    elif(keyboard.is_pressed('end')):
        break
