# The audio signal, full-wave rectified audio signal, half-wave rectified audio signal, and added offset audio signal:

import sounddevice as sd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np

master = tk.Tk()
master.geometry("1500x1500")
master.title("MY VOİCE WAVE")
record_time = tk.DoubleVar()

fs = 44100

def voice_rec():
    global myrecord
    global time
    
    # seconds
    duration = float(record_time.get())
    myrecord =  sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    time=np.linspace(0,len(myrecord)/fs,num=len(myrecord))
    sd.wait()
    
    plt.cla()
    fig,a2=plt.subplots(figsize=(9,4))
    plt.plot(time,myrecord, color="blue")
    plt.xlabel('time',fontsize=15)
    plt.ylabel('Amplitude',fontsize=15)
    plt.title('My Voice Wave',fontsize=20, y=1.03)
    plt.show()
    
    canvas2 = FigureCanvasTkAgg(fig, master=master)
    canvas2.get_tk_widget().grid(row = 0, column = 3)
    canvas2.draw()
    plt.close("all")

def func(): 
    plt.cla()
    if numbers.get() == 1:
        # I made a full wave.
        myrecording2=np.abs(myrecord)
        
        fig,a3=plt.subplots(figsize=(9,4))
        plt.plot(time,myrecording2,color='red')
        plt.title('Full Wave', fontsize=20, y=1.03)
        plt.xlabel('Time', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.show()
        print(myrecording2)

    elif numbers.get() == 2:
        # I made a half wave, leaving only the positive ones.
        # reset the negative sign ones.
        myrecording3=myrecord.clip(0)
        
        fig,a4=plt.subplots(figsize=(9,4))
        plt.plot(time,myrecording3,color='red')
        plt.title('Half Wave', fontsize=20, y=1.03)
        plt.xlabel('Time', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.show()
        print(myrecording3)

    elif numbers.get()==3:
        # With OFFSET added:
        # I found the min value of the audio recording and subtracted it from the normal audio recording.
        myrecording4=myrecord.min()
        my=myrecord-myrecording4
        
        fig,a5=plt.subplots(figsize=(9,4))
        plt.plot(time,my,color='red')
        plt.title('OFFSET', fontsize=20, y=1.03)
        plt.xlabel('Time', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.show()
        print(my)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.get_tk_widget().grid(row = 4, column = 3)
    canvas.draw()
    plt.close("all")

numbers = tk.IntVar()

r1 = tk.Radiobutton(master, text="Full Wave", variable=numbers, value=1, font = "Verdana 15 bold")
r1.grid(row=3, column=0, padx=5)
r2 = tk.Radiobutton(master, text="Half Wave", variable=numbers, value=2, font = "Verdana 15 bold")
r2.grid(row=4, column=0, padx=5)
r3 = tk.Radiobutton(master, text="Offset Wave", variable=numbers, value=3, font = "Verdana 15 bold")
r3.grid(row=5, column=0, padx=20)
     
d = tk.Button(master, text="RUN", command=func, fg = "blue", font = "Verdana 15 bold")
d.grid(row=6, column=0, padx=5)  
   
a = tk.Label(master, text=" Voice Recoder : ", padx = 50, fg = "blue", bg = "yellow", font = "Verdana 20 bold")

a.grid(row=0, column=0, padx=5)

b = tk.Entry(master, textvariable=record_time, font = "Verdana 10 bold")
b.grid(row=1,column=0, padx=5, pady=5, ipady=5)

c = tk.Button(master, text="START RECORD", command=voice_rec, fg = "blue", font = "Verdana 15 bold")
c.grid(row=2, column=0, padx=5)  

master.mainloop()
