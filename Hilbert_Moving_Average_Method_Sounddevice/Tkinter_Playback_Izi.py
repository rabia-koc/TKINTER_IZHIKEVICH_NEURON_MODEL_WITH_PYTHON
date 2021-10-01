import sounddevice as sd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import matplotlib

matplotlib.use("TkAgg")
import numpy as np
from scipy import signal
import warnings

warnings.filterwarnings("ignore")

master = tk.Tk()
master.title("IZHIKEVİCH MODELS")
master.geometry("1120x1120")

record_time = tk.DoubleVar()
h = 0.2
fs = 44100
w = int(fs / 100)

def voice_rec():
    global downresampled, downresampledt, timerecord, result, record, duration

    duration = float(record_time.get())
    record = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()
    resrec = record.reshape(int(duration * fs * 2))
    rec1 = np.copy(resrec)

    timerecord = np.linspace(0, int(duration), num=len(resrec))

    stdm = 3 * np.std(resrec[:441])

    for i in range(len(resrec)):
        if resrec[i] <= stdm and resrec[i] >= -stdm:
            resrec[i] = 0

    myrecord = np.abs(resrec)

    # analytic_signal = signal.hilbert(resrec)
    # result = np.abs(analytic_signal)

    sum = 0
    result = np.ones(len(myrecord))
    for i in range(0, w):
        sum = sum + myrecord[i]
        result[i] = sum / (i + 1)
    for i in range(w, len(myrecord)):
        sum = sum - myrecord[i - w] + myrecord[i]
        result[i] = sum * 2 / w

    plt.cla()
    fig, a1 = plt.subplots(figsize=(13, 4))
    a1.plot(timerecord, rec1, color='purple', label='Original Voice')
    a1.plot(timerecord, myrecord, color='orange', label='Full Voice')
    a1.plot(timerecord, result, color='black', label='Filtered Voice')
    a1.set_title('Record')
    a1.set_xlabel('time(s)')
    a1.set_ylabel('Amplitude')
    a1.legend(loc=3)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.get_tk_widget().place(x=350, y=20)
    plt.close("all")

    downresampled = signal.resample(result, int(duration * 5000))
    downresampledt = np.linspace(0, int(duration), num=len(downresampled))


def Discrete_Model(a, b, u, v, I):
    v = v + h * (0.04 * v * v + 5 * v + 140 - u + I)
    u = u + h * (a * (b * v - u))
    return u, v


def Izhikevich(a, b, c, d):
    global v
    v = -65 * np.ones((len(downresampledt)))
    u = 0 * np.ones((len(downresampledt)))
    u[0] = b * v[0]

    I = downresampled * 10   # The scale can be changed.

    for k in range(0, len(downresampledt) - 1):
        u[k + 1], v[k + 1] = Discrete_Model(a, b, u[k], v[k], I[k])
        if v[k + 1] > 30:
            v[k + 1] = c
            u[k + 1] = u[k + 1] + d
    plot_input_output(downresampledt, v, I, a, b, c, d)


def playsback():
    upresampled = signal.resample(v, int(duration * fs))
    sd.play(upresampled, fs)


def plot_input_output(timerecord, v, I, a, b, c, d):
    plt.cla()
    fig, ax1 = plt.subplots(figsize=(13, 4))
    ax1.plot(timerecord, v, 'b-', label='Output')
    ax1.set_xlabel('time(ms)')
    ax1.set_ylabel('Output mV', color='b')

    ax1.tick_params('y', colors='b')
    ax1.set_ylim(-95, 45)
    ax2 = ax1.twinx()
    ax2.plot(timerecord, I, 'black', label='Result Voice')

    ax2.set_ylabel('Result Voice', color='black')
    ax2.set_ylim(0, 100)
    ax2.tick_params('y', colors='black')
    plt.close("all")

    fig.tight_layout()
    ax1.legend(loc=1)
    ax2.legend(loc=2)
    ax1.set_title('Parameters a %s b: %s c: %s d: %s' % (a, b, c, d))

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.get_tk_widget().place(x=350, y=450)
    plt.close("all")


def func():
    print(number.get(), " seçildi...")

    if number.get() == 1:
        Izhikevich(0.02, 0.2, -65, 8)
    elif number.get() == 2:
        Izhikevich(0.1, 0.2, -65, 2)
    elif number.get() == 3:
        Izhikevich(0.02, 0.2, -55, 4)


number = tk.IntVar()

r1 = tk.Radiobutton(master, text="Regular Spiking", variable=number, value=1, font="Verdana 15 bold")
r1.place(x=20, y=485)
r2 = tk.Radiobutton(master, text="Fast Spiking", variable=number, value=2, font="Verdana 15 bold")
r2.place(x=20, y=545)
r3 = tk.Radiobutton(master, text="Intrinsically Bursting", variable=number, value=3, font="Verdana 15 bold")
r3.place(x=20, y=605)

label1 = tk.Label(master, text='Izhikevich Neuron Models', fg="brown", bg="white", font="Verdana 15 bold")
label1.place(x=20, y=420)

a = tk.Label(master, text=" Voice Recoder  : ", padx=50, fg="brown", bg="white", font="Verdana 15 bold")
a.place(x=27, y=120)

b = tk.Entry(master, width=15, textvariable=record_time, font="Verdana 15 bold")
b.place(x=28, y=160)

c = tk.Button(master, text="START RECORD", width=15, command=voice_rec, fg="dark green", font="Verdana 15 bold")
c.place(x=20, y=200)

d = tk.Button(master, text="RUN IT", width=15, command=func, fg="dark green", font="Verdana 15 bold")
d.place(x=20, y=665)

e = tk.Button(master, text="PLAY", width=15, command=playsback, fg="dark green", font="Verdana 15 bold")
e.place(x=20, y=720)


master.mainloop()



