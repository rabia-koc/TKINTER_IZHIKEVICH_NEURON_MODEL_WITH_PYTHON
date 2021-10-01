import tkinter as tk
import sounddevice as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

master = tk.Tk()
w = master.winfo_screenwidth()
h = master.winfo_screenheight()
master.geometry("%dx%d" % (w, h))
master.title("IZHIKEVİCH MODELS")

h = 0.1
fs = 44100
w = int(fs / 100)

a_copy = np.zeros((44100))
process = np.zeros((44100))
b_copy = np.zeros((44100))
rec1 = np.zeros((44100))
duration = 1

def start():
    global running, reccord
    running = True
    reccord = sd.rec(int(0.1 * fs), samplerate=fs, channels=1)
    sd.wait()
    voice_rec()

def stop():
    global running
    running = False

def voice_rec():
    global downresampled, downresampledt, timerecord, result, record, process, total, total2, b_copy, a_copy

    if running:
        record = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        rec1 = np.copy(record)  # we make a copy without putting the sound into the signal.
        process = filtering(record)  # we filter the recorded sound.
        total = np.append(a_copy, process)  # We added the filtered audio and the empty array together.
        total2 = np.append(b_copy, rec1)  # We added the recorded audio copy and the empty array together.
        timerecord = np.linspace(0, int(2 * duration), num=len(total))


        fig, ax1 = plt.subplots(figsize=(13, 5))
        ax1.plot(timerecord, total2, color='red')
        ax1.plot(timerecord, total, color='black')
        ax1.set_title('Record')
        ax1.set_xlabel('time(s)')
        ax1.set_ylabel('Amplitude')

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.get_tk_widget().place(x=280, y=140)

        canvas.draw()
        plt.close("all")
        # update after drawing
        b_copy = rec1
        a_copy = process

    master.after(1, voice_rec)


def filtering(record):
    global result, reccord

    stdm = 3 * np.std(reccord[:441])
    for i in range(len(record)):
        if record[i] <= stdm and record[i] >= -stdm:
            record[i] = 0
    myrecord = np.abs(record)
    sum = 0
    result = np.ones(len(myrecord))
    for i in range(0, w):
        sum = sum + myrecord[i]
        result[i] = sum / (i + 1)
    for i in range(w, len(myrecord)):
        sum = sum - myrecord[i - w] + myrecord[i]
        result[i] = sum * 2 / w
    return result

    downresampled = signal.resample(result, int(duration * 10000))
    downresampledt = np.linspace(0, int(duration), num=len(downresampled))


stop = tk.Button(master, text='STOP', command=stop, width=15, font = "Verdana 15 bold", fg = "blue").place(x=27, y=345)
c = tk.Button(master, text="START RECORD", width=15, command=start, font = "Verdana 15 bold", fg = "blue")
c.place(x=27, y=290)

master.mainloop()
