import tkinter as tk
import sounddevice as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import threading

master=tk.Tk()
w=master.winfo_screenwidth()
h=master.winfo_screenheight()
master.geometry("%dx%d" % (w,h))
master.title("IZHIKEVİCH MODELS")

h=0.1    
fs=44100   
w=int(fs/100) 

def start():
    global running,reccord, stdm, result, status
    running = True
    reccord=sd.rec(int(1.5*fs),samplerate=fs,channels=1)
    status = sd.wait()
    stdm=3*np.std(reccord[:441]) 
    thread()

def thread():
    if running:
        t1=threading.Thread(target=voice_rec())
        t2=threading.Thread(target=raise_())
        t3=threading.Thread(target=filtering())
        t4=threading.Thread(target=plot_filtering())
        t5=threading.Thread(target=func())
        t6=threading.Thread(target=playsback())
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
    master.after(1,thread)
     
def voice_rec():
    global  res, status
    res = sd.rec(int(0.5* fs), samplerate=fs, channels=1)  
    status = sd.wait()

def raise_():
    global timerecord, reccord
    reccord=np.append(reccord[-66150:],res)
    timerecord=np.linspace(0,2, num=len(reccord)) 

def filtering():
    global result, downresampled, downresampledt                                
    for i in range(len(reccord)):   
        if reccord[i]<=stdm and reccord[i]>=-stdm : 
            reccord[i]=0                   
    myrecord=np.abs(reccord) 
    sum = 0
    result=np.ones(len(myrecord))  
    for i in range( 0, w ):        
        sum = sum + myrecord[i]    
        result[i] = sum / (i+1)    
    for i in range( w, len(myrecord) ):   
        sum = sum - myrecord[i-w] + myrecord[i]  
        result[i] = sum*2 / w           
        
def plot_filtering():
    global  downresampled, downresampledt
    ax1.clear()
    ax1.plot(timerecord,reccord,color='turquoise')
    plt.close("all")
    ax1.plot(timerecord,result,'black')
    #ax1.legend(loc=3)
    ax1.set_xlabel('Time(s)',fontsize=7)
    ax1.set_ylabel('Amplitude',color='r') 
    ax1.tick_params('y',colors='r')
    canvas2.draw()
    
    downresampled=signal.resample(result, int(4410*2))
    downresampledt=np.linspace(0, int(2), num=len(downresampled))
    
def Discrete_Model(a,b,u,v,I):
    v=v+h*(0.04*v*v+5*v+140-u+I)         
    u=u+h*(a*(b*v-u))                    
    return u,v                           

def Izhikevich(a,b,c,d):
    global v
    v=-65*np.ones((len(downresampledt))) 
    u=0*np.ones((len(downresampledt)))   
    u[0]=b*v[0]

    I=downresampled*10/max(downresampled)

    for k in range(0,len(downresampledt)-1):
        u[k+1],v[k+1]=Discrete_Model(a,b,u[k],v[k],I[k])
        if v[k+1]>30:
            v[k+1]=c                     
            u[k+1]=u[k+1]+d
    plot_input_output(downresampledt,v,I,a,b,c,d)


def plot_input_output(timerecord,v,I,a,b,c,d):
    ax2.clear()
    ax3.clear()
    ax3.plot(timerecord,v,'b-',label='Output')
    plt.close("all")
    ax3.set_xlabel('time(ms)',fontsize=7)
    ax3.set_ylabel('Output mV',color='b')
    ax3.tick_params('y',colors='b')
    ax3.set_ylim(-95,45)
    ax2.plot(timerecord,I,'black',label='Result Voice')
    ax2.set_ylabel('Result Voice',color='black')
    ax2.set_ylim(0,100)
    ax2.tick_params('y',colors='black')
    fig.tight_layout()
    #ax2.legend(loc=1)
    #ax3.legend(loc=2)
    ax2.set_title('Parameters a %s b: %s c: %s d: %s' %(a,b,c,d))
    canvas.draw()
    plt.close("all")


def func(): 
    if number.get() == 1: 
        Izhikevich(0.02, 0.2, -65, 8) 
    elif number.get() == 2:
        Izhikevich(0.1, 0.2, -65, 2) 
    elif number.get() == 3:
        Izhikevich(0.02, 0.2, -55, 4) 
        
def stop():
    global running
    running = False
    
def playsback():
    upresampled=signal.resample(v, int(2*fs))
    sd.play(upresampled, fs,blocking=True)


fig,ax3=plt.subplots(figsize=(11.5,3.4))
ax2=ax3.twinx()
fig2,ax1=plt.subplots(figsize=(11.5,3.4))
canvas=FigureCanvasTkAgg(fig, master=master)
canvas.get_tk_widget().place(x=350,y=400)
canvas2=FigureCanvasTkAgg(fig2,master=master)
canvas2.get_tk_widget().place(x = 350, y = 25)
plt.close("all")
number = tk.IntVar()
    
r1 = tk.Radiobutton(master, text="Regular Spiking", variable=number, value=1, font = "Verdana 15 bold")
r1.place(x=20,y=485)
r2 = tk.Radiobutton(master, text="Fast Spiking", variable=number, value=2, font = "Verdana 15 bold")
r2.place(x=20,y=525)
r3 = tk.Radiobutton(master, text="Intrinsically Bursting", variable=number, value=3, font = "Verdana 15 bold")
r3.place(x=20,y=565)
         
label1= tk.Label(master, text = 'Izhikevich Neuron Models', fg = "blue", bg = "white", font = "Verdana 15 bold")
label1.place(x=20,y=440)
      
stop=tk.Button(master,text='STOP',command=stop, width=15, font = "Verdana 15 bold").place(x=27,y=175)
c = tk.Button(master, text="START RECORD",width=15, command=lambda:[start()], font = "Verdana 15 bold").place(x=27,y=120)
    
master.mainloop()