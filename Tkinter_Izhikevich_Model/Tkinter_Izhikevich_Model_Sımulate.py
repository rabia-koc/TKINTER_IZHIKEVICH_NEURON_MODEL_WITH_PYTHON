import tkinter as tk
from tkinter import *
import tkinter.font as font

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import sys
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

h =0.5
input_onset=300
input_amp=5

time = np.arange(0,1000.1,h)

def Input(input_onset,input_amp):
    I=np.zeros((len(time)))
    for k in range(0,len(time)):
        if time[k]>input_onset:
            I[k]=input_amp
    return I

def Discrete_Model(a,b,u,v,I):
    v=v+h*(0.04*v*v+5*v+140-u+I)
    u=u+h*(a*(b*v-u))
    return u,v

def Izhikevich(a,b,c,d):
    v=-65*np.ones((len(time)))
    u=0*np.ones((len(time)))
    u[0]=b*v[0]

    I=Input(input_onset,input_amp)
    for k in range(0,len(time)-1):
        u[k+1],v[k+1]=Discrete_Model(a,b,u[k],v[k],I[k])
        if v[k+1]>30:
            v[k+1]=c
            u[k+1]=u[k+1]+d
    plot_input_output(time,v,I,a,b,c,d)

canvas=[]
def forget_canvas():
    try:
        canvas.get_tk_widget().pack_forget()
    except AttributeError:
        pass

def plot_input_output(time,v,I,a,b,c,d):

    forget_canvas()
    fig,ax1=plt.subplots(figsize=(12,3))
    ax1.plot(time,v,'b-',label='Output')
    ax1.set_xlabel('time(ms)')
    ax1.set_ylabel('Output mV',color='b')
    ax1.tick_params('y',colors='b')
    ax1.set_ylim(-95,40)
    ax2=ax1.twinx()
    ax2.plot(time,I,'r',label='Input')
    ax2.set_ylim(0,input_amp*20)
    ax2.set_ylabel('Input(mV)',color='r')
    ax2.tick_params('y',colors='r')

    fig.tight_layout()
    ax1.legend(loc=1)
    ax1.legend(loc=3)
    ax1.set_title('Parameters a %s b: %s c: %s d: %s' %(a,b,c,d))

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.get_tk_widget().grid(row = 2, column = 3)

    canvas.draw()
    plt.close("all")

win =tk.Tk()

win.title('Izhikevich Model')
win.geometry("1150x700")
win.wm_attributes("-topmost",1)   # keeps the window on the screen.
win.resizable(True, False)        # only transverse sizing happens.

# I placed the parameters of the Izhikevich models on the radiobuttons.
def function():
    print(numbers.get(), " seçildi...")
    
    if numbers.get() == 1:
        Izhikevich(0.02, 0.2, -65, 8) # RS(regular spiking)
    elif numbers.get() == 2:
        Izhikevich(0.1, 0.2, -65, 2) # FS(fast spiking)
        
    elif numbers.get() == 3:
        Izhikevich(0.02, 0.2, -55, 4)  # IB(intrinsically bursting)


numbers = tk.IntVar()

r1 = tk.Radiobutton(win, text="RS", variable=numbers, bg='#dda0dd', font = "Verdana 15 bold", height=4, width=20, value=1)
r1.grid(row=1,column=0)

r2 = tk.Radiobutton(win, text="FS", variable=numbers, bg='#dda0dd', font = "Verdana 15 bold", height=4, width=20, value=2)
r2.grid(row=2,column=0)

r3 = tk.Radiobutton(win, text="IB", variable=numbers, bg='#dda0dd', font = "Verdana 15 bold", height=4, width=20, value=3)
r3.grid(row=3,column=0)

my_button=tk.Button(win, text="SIMULATE",width=34,height=4, command=function, fg = "green", bg="white", font = "Verdana 15 bold").grid(row=4,column=0)

win.mainloop()
