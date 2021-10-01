import sounddevice as sd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np
from scipy import signal
import warnings
warnings.filterwarnings("ignore")
# Import of libraries.

master=tk.Tk()
master.title("IZHIKEVİCH MODELS")
master.geometry("1200x1200")

record_time = tk.DoubleVar()
h=0.2       # step size
fs=44100    # frequency value
w=int(fs/100) # my window range is for moving average

def voice_rec():
    global downresampled,downresampledt,timerecord,result,record
    
    duration = float(record_time.get())   # I created my time input duration in float.
    record = sd.rec(int(duration * fs), samplerate=fs,channels=2,dtype='float64')  
    sd.wait()                                 # my voice has been recorded so far.
    resrec=record.reshape(int(duration*fs*2)) # I defined the audio signal in 2 dimensions.
    rec1=np.copy(resrec)                      # I made a copy of my original signal to have it plotted.
    
    timerecord=np.linspace(0,int(duration),num=len(resrec))  # I defined time in 1 dimension.

    # I calculated a threshold value for 3 times the standard deviation
    # I did it for the first 0.01 seconds.
    # I set the values below the threshold value to 0.
    stdm=3*np.std(resrec[:441]) 
    
    for i in range(len(resrec)):   
        if resrec[i]<=stdm and resrec[i]>=-stdm : 
            resrec[i]=0               
            
    myrecord=np.abs(resrec) # I got the full wave of my 2D signal

    sum = 0
    result=np.ones(len(myrecord))  # I created an array of 1's in length myrecord.
    for i in range( 0, w ):        # I looked at the place from 0 to w and averaged in order.
        sum = sum + myrecord[i]    # I did the collection.
        result[i] = sum / (i+1)    # I took the average of the collected values and added it to the result.
    for i in range( w, len(myrecord) ):   # I got it from the window to the length of myrecord.
        sum = sum - myrecord[i-w] + myrecord[i]  # I did the slide pick-up every time.
        result[i] = sum*2 / w                    # Then I took the average of all the values.
# Finally, I made it ready for drawing by adding it to the result.

    plt.cla()      # I cleared the current active graphics.
    fig,a1=plt.subplots(figsize=(13,4))  
    a1.plot(timerecord,rec1,color='purple',label='Original Voice') # I drew the original sound.
    a1.plot(timerecord,myrecord,color='orange',label='Full Voice')  # I drew the full-wave received sound.
    a1.plot(timerecord,result,color='black',label='Filtered Voice') # I drew the filtered version.
    a1.set_title('Record - Moving Average Method')
    a1.set_xlabel('time(s)')  
    a1.set_ylabel('Amplitude')
    a1.legend(loc=3) # label where to write my names

    # to draw on the window screen.
    canvas=FigureCanvasTkAgg(fig,master=master)
    canvas.get_tk_widget().place(x=350,y=20)  # I determined the place where my figure will be drawn.
    plt.close("all")  # I closed the figures outside my window.

    # (1,1000 0.2 steps)
    # number of samples: at 1000/0.2=5000 sec
    # My record signal is currently taking 44100 samples.
    # I need to set it to 5000.
    # 44100/5000=8.82=9
    # so I'll take 1 out of every 9 samples.
    # so I gave h=0.2.
    
    downresampled=result[::9]   # I downsample my signal.
    downresampledt=timerecord[::9] # I downsample my signal time.
    
def Discrete_Model(a,b,u,v,I):
    v=v+h*(0.04*v*v+5*v+140-u+I)         # discrete membrane potential form neuron.
    u=u+h*(a*(b*v-u))                    # discrete form within the membrane recovery variable.
    return u,v                           # u is a recovery variable.
# The change in v at any time depends on the step u and u on the step v at any time.

def Izhikevich(a,b,c,d):
    v=-65*np.ones((len(downresampledt))) # setting the initial values of the membrane potential.
    u=0*np.ones((len(downresampledt)))   # sets the initial value of the membrane recovery.
    u[0]=b*v[0]                          # initial state
    
    I=downresampled*10                  # The scale can be changed.
    
    for k in range(0,len(downresampledt)-1):
        u[k+1],v[k+1]=Discrete_Model(a,b,u[k],v[k],I[k])
        if v[k+1]>30:
            v[k+1]=c                     # reset voltage.
            u[k+1]=u[k+1]+d              # update process.
    plot_input_output(downresampledt,v,I,a,b,c,d)

def plot_input_output(timerecord,v,I,a,b,c,d):
    plt.cla()
    fig,ax1=plt.subplots(figsize=(13,4))
    ax1.plot(timerecord,v,'b-',label='Output')
    ax1.set_xlabel('time(ms)')
    ax1.set_ylabel('Output mV',color='b')
    ax1.tick_params('y',colors='b')
    ax1.set_ylim(-95,45)
    ax2=ax1.twinx()
    ax2.plot(timerecord,I,'black',label='Result Voice')
    
    ax2.set_ylabel('Result Voice',color='black')
    ax2.set_ylim(0,100)
    ax2.tick_params('y',colors='black')
    plt.close("all")
    
    fig.tight_layout()
    ax1.legend(loc=1)
    ax2.legend(loc=2)
    ax1.set_title('Parameters a %s b: %s c: %s d: %s' %(a,b,c,d))

    canvas=FigureCanvasTkAgg(fig, master=master)  # izhikevich and result for drawing my signal inside the window.
    canvas.get_tk_widget().place(x=350,y=450)
    plt.close("all")

def func(): 
    print(number.get(), " seçildi...")
    
    if number.get() == 1: 
        Izhikevich(0.02, 0.2, -65, 8) # RS named izhikevich parameters.
    elif number.get() == 2:
        Izhikevich(0.1, 0.2, -65, 2) # FS named izhikevich parameters.
        
    elif number.get() == 3:
        Izhikevich(0.02, 0.2, -55, 4)  # IB named izhikevich parameters.

number = tk.IntVar()

r1 = tk.Radiobutton(master, text="Regular Spiking", variable=number, value=1, font = "Verdana 15 bold")
r1.place(x=20,y=485)
r2 = tk.Radiobutton(master, text="Fast Spiking", variable=number, value=2, font = "Verdana 15 bold")
r2.place(x=20,y=545)
r3 = tk.Radiobutton(master, text="Intrinsically Bursting", variable=number, value=3, font = "Verdana 15 bold")
r3.place(x=20,y=605)
     
label1= tk.Label(master, text = 'Izhikevich Neuron Models', fg = "blue", bg = "white", font = "Verdana 15 bold")
label1.place(x=20,y=420)
  
a = tk.Label(master, text=" Voice Recoder  : ", padx = 50, fg = "blue", bg = "white", font = "Verdana 15 bold")  # determining the name to enter my time.
a.place(x=27,y=120)                  

b = tk.Entry(master, width=15,textvariable=record_time, font = "Verdana 15 bold")  # where I will enter my time.
b.place(x=28,y=160)

c = tk.Button(master, text="START RECORD",width=15, command=voice_rec, fg = "purple", font = "Verdana 15 bold")  # My button to start my recording.
c.place(x=20,y=200)

d = tk.Button(master, text="RUN IT", width=15, command=func, fg = "purple", font = "Verdana 15 bold")   # The button that makes one of the radiobuttons that I will choose in Izhikevich work.
d.place(x=20,y=665)

master.mainloop()