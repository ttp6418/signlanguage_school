import speech_recognition as sr
import numpy as np
import sys
import warnings
import sounddevice as sd
import os
import tkinter
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import PIL
from PIL import Image
from PIL import ImageTk
import threading
import cv2
import time
import pyaudio
import wave
from google.cloud import speech
import grpc
import io

global audio_active
global audio_stop_active
global read_active
# global video_active

# global audio_name

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
np.set_printoptions(threshold=sys.maxsize)

audio_active = False
audio_stop_active = False
read_active = False
video_active = False
mod = 0
mod_list = ['스테레오믹스', '마이크', '로컬파일']
audio_name = None

audio_curr = None

print(os.getcwd())

def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('__file__')))
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def onDraw():
    global mainWindow
    global mode
    global output
    
    global text

    mainWindow = tkinter.Tk()
    mainWindow.title("수어번역기")
    mainWindow.geometry("530x700+40+40")
    mainWindow.resizable(False, False)
    mainWindow.iconphoto(False, tkinter.PhotoImage(file=resource_path('./main.png')))
    # mainWindow.iconphoto(False, tkinter.PhotoImage(file=os.getcwd() + ('/program/main.png')))

    notebook = tkinter.ttk.Notebook(mainWindow, width=510, height=460)
    notebook.place(x=10, y=80)

    # importIcon = PhotoImage(file=resource_path('./import.png'))
    recIcon = PhotoImage(file=resource_path('./rec.png'))
    # recIcon = PhotoImage(file=os.getcwd() + ('/program/rec.png'))

    menubar = Menu(mainWindow)
    optionmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="메뉴", menu=optionmenu)
    optionmenu.add_command(label="나가기", command=mainWindow.quit)
    mainWindow.config(menu=menubar)

    mode = tkinter.IntVar()
    rad1 = tkinter.Radiobutton(mainWindow, text =mod_list[0], variable = mode, value = 0, command = onMode)
    rad1.grid(row=1, column=0, sticky = "w")
    rad2 = tkinter.Radiobutton(mainWindow, text =mod_list[1], variable = mode, value = 1,command = onMode)
    rad2.grid(row=2, column=0, sticky = "w")
    # rad3 = tkinter.Radiobutton(mainWindow, text =mod_list[2], variable = mode, value = 2, command = onMode)
    # rad3.grid(row=3, column=0, sticky = "w")

    #seperator1 = tkinter.ttk.Separator(mainWindow, orient="vertical")
    #seperator1.place(x=100, y=0, relwidth=0, relheight=1)

    """output = tkinter.IntVar()
    rad4 = tkinter.Radiobutton(mainWindow, text ='텍스트', variable = output, value = 0, command = onOutput)
    rad4.grid(row=1, column=1, sticky = "w")
    rad5 = tkinter.Radiobutton(mainWindow, text ='수어', variable = output, value = 1,command = onOutput)
    rad5.grid(row=2, column=1, sticky = "w")"""

    recButton = tkinter.Button(mainWindow, text="음성 인식 시작", command=onRec_start, image=recIcon, compound=LEFT)
    recButton.place(x=250, y=50)

    stopButton = tkinter.Button(mainWindow, text="음성 인식 종료", command=onRec_stop)
    stopButton.place(x=400, y=50)

    #loadButton = tkinter.Button(mainWindow, text="파일 불러오기", command=onLoad, image=importIcon, compound=LEFT)
    #loadButton.place(x=550, y=10)

    exitButton = tkinter.Button(mainWindow, text="나가기", command=mainWindow.quit)
    exitButton.place(x=400, y=10)

    frame1 = tkinter.Frame(mainWindow)
    notebook.add(frame1, text="텍스트번역")
    #frame2 = tkinter.Frame(mainWindow)
    #notebook.add(frame2, text="수어번역")

    text = tkinter.Text(frame1, width=70, height=33)
    text.insert(tkinter.CURRENT, "이곳에 번역된 텍스트가 입력됩니다.")
    text.place(x=10, y=10)

    logo = cv2.imread(resource_path('./aivle.jpg'))
    TKImage_logo = cv2.cvtColor(cv2.resize(logo, (100,50)), cv2.COLOR_BGR2RGB)  # TKinter는 RGB중심
    TKImage_logo = PIL.Image.fromarray(TKImage_logo)  # numpy 배열을 이미지객체화
    imgtk_logo = PIL.ImageTk.PhotoImage(image=TKImage_logo)  # TKinter와 호완되는 이미지객체화

    label_logo = tkinter.Label(mainWindow, image=imgtk_logo)
    label_logo.place(x=20, y=600)

    text_logo = tkinter.Text(mainWindow, width=40, height=1)
    text_logo.insert(tkinter.CURRENT, 'http://127.0.0.1:8000/')
    text_logo.configure(state='disabled')
    text_logo.place(x=140, y=600)

    mainWindow.mainloop()

def onRec():
    global audio_active
    global audio_stop_active

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 3600
    WAVE_OUTPUT_FILENAME = os.getcwd() + '/temp.wav'
    print(WAVE_OUTPUT_FILENAME)
    # C:\Users\82107\AppData\Local\Temp\_MEI182522\./temp.wav

    p = pyaudio.PyAudio()

    host_info = p.get_host_api_info_by_index(0)
    device_mic = host_info.get('defaultInputDevice')
    device_count = host_info.get('deviceCount')
    devices = []

    # iterate between devices:
    for i in range(0, device_count):
        device = p.get_device_info_by_host_api_device_index(0, i)
        devices.append(device['name'])
        if device['name'] == '스테레오 믹스(Realtek(R) Audio)' or device['name'] == 'Stereo Mix (Realtek(R) Audio)':
            device_stereo = i

    while(1):
        while(audio_active):
            audio_active = False
            if mod == 0:
                stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = device_stereo,
                    frames_per_buffer = CHUNK)
            elif mod == 1:
                stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = device_mic,
                    frames_per_buffer = CHUNK)
            elif mod == 2:
                pass
            if mod == 1 or mod == 0:
                print("* recording")
                frames = []
                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                    if audio_stop_active:
                        audio_stop_active=False
                        break
                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                print("* done recording")
                stream.stop_stream()
                stream.close()
                p.terminate()
                wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
            else: pass

def onRead():
    global read_active
    global text

    recognizer = sr.Recognizer()

    while(1):
        time.sleep(2)
        while(read_active):
            if mod == 2:
                if audio_name: recog_audio = audio_name
                else: 
                    messagebox.showinfo('알림창', '현재 선택된 로컬파일이 없습니다.')
                    read_active = False
                    continue
            else:
                recog_audio = os.getcwd() + '/temp.wav'
            try: 
                file = sr.AudioFile(recog_audio)

                with file as source:
                    audio = recognizer.record(source)
                string = recognizer.recognize_google(audio_data=audio, language="ko")
                text.delete(1.0, END)
                text.insert(tkinter.CURRENT, string)
            except: pass
            """if video_active: # 수어번역인데 방향성에 안맞음
                pass
            else:
                pass"""

"""def onLoad():
    global audio_name
    if mod == 2:
        Tk.filename = filedialog.askopenfilename(initialdir=str(os.path.dirname(os.getcwd())) + '/', title="오디오 선택", filetypes=(("all files", "*.*"), ("raw files", "*.raw")))
        audio_name = str(Tk.filename)
    else: messagebox.showinfo('알림창', '모드 선택을 확인해주세요. 현재 모드 : ' + mod_list[mod])"""

def onRec_start():
    global audio_active
    global read_active
    audio_active=True
    read_active = True

def onRec_stop():
    global audio_stop_active
    global read_active
    audio_stop_active=True
    read_active = False

def onMode():
    global mod
    global read_active
    if mode.get() == 0: mod = 0
    elif mode.get() == 1: mod = 1
    # elif mode.get() == 2: mod = 2

"""def onOutput():
    global outpu
    global video_active
    if output.get() == 0: outpu = 0; video_active = False
    elif output.get() == 1: outpu = 1; video_active = True"""

drawThread = threading.Thread(target=onDraw)
drawThread.start()

audioThread = threading.Thread(target=onRec)
audioThread.daemon = True
audioThread.start()

readThread = threading.Thread(target=onRead)
readThread.daemon = True
readThread.start()