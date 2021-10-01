import pyaudio
import struct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk

win=tk.Tk()
w=win.winfo_screenwidth()
h=win.winfo_screenheight()
win.geometry("%dx%d" % (w,h))
win.title("Izhikevich Model")

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16

CHUNK = int(44100/20)
stream = mic.open(format=FORMAT, channels=1, rate=44100, input=True, output=True, frames_per_buffer=CHUNK)

fig, ax = plt.subplots(figsize=(14,6))
x = np.arange(0, 2 * CHUNK, 2)
ax.set_ylim(-200, 200)
ax.set_xlim(0, CHUNK) # make sure our x axis matched our chunk size
line, = ax.plot(x, np.random.rand(CHUNK))
canvas=FigureCanvasTkAgg(fig, master=win) 
canvas.get_tk_widget().place(x=10,y=100)
canvas.draw()

while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(data, np.int16)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

win.mainloop()