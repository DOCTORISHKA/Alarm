import time
import mss
import pyaudio
import os
import wave
import keyboard
import threading
import queue
from threading import Thread


startBtn = "page down"
resetBtn = "pause"
endBtn = "end"


global timer
global thread_stop
global thread_1
global thread_2


lock = threading.Lock()
thread_2 = []
counter = 0
#q = queue.Queue()


def create_thread(task):
    return Thread(target=task)


def create_timer(ltime, func):
    return threading.Timer(ltime, func)


def PlayAudio():
    audio_file = wave.open("sample.wav")
    FORMAT = audio_file.getsampwidth() # глубина звука
    CHANNELS = audio_file.getnchannels() # количество каналов
    RATE = audio_file.getframerate() # частота дискретизации
    N_FRAMES = audio_file.getnframes() # кол-во отсчетов
    audio = pyaudio.PyAudio()
    out_stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, output=True)
    out_stream.write(audio_file.readframes(N_FRAMES))  # отправляем на динамик
    out_stream.close()


def Countdown():
    print("cmon bro")
    t = []
    timer = 60.0
    def on_exists(fname: str) -> None:
        if os.path.isfile(fname):
            global counter
            counter += 1
            newfile = str(counter) + " " + f"{fname}"
            print(f"{fname} -> {newfile}")
            os.rename(fname, newfile)
    with mss.mss() as sct:
        filename = sct.shot(output="mon-{mon}.png", callback=on_exists)
        print(filename)
    t.append(create_timer(timer, PlayAudio))
    t[0].start()
    t[0].join()
    t.clear()


def InputListening():
    thread_stop = False
    while(True):
        time.sleep(0.004)
        if(keyboard.is_pressed(startBtn)):
            thread_2.append(create_thread(Countdown()))
            thread_2[0].start()
            thread_2[0].join()
            thread_2.clear()
        #elif(keyboard.is_pressed(resetBtn)):
            #q.put(threading.cancel())
            #return thread_stop
        elif(keyboard.is_pressed(endBtn)):
            thread_stop = True
            return thread_stop
        if thread_stop == True:
            return 0


thread_1 = Thread(target=InputListening, daemon=True)
thread_1.start()
thread_1.join()
