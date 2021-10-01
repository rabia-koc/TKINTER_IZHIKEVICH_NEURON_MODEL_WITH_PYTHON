"""
Model; It is a system of two first-order nonlinear differential equations.

dV/dt = 0.04V^2 + 5V + 140 - u + I,
du/dt = a(bV - u)

Where u and v are dimensionless variables, I is the input of the system
and a and b are immeasurable parameters manipulated to describe different ignition patterns.
The variable v is most interesting as it represents the membrane potential of the microvolt neuron (mV).
Represents a membrane recovery variable that explains the activation of u.
K^+ ionic currents and inactivation Na^+ ionic currents and provide negative feedback.
After reaching the spike peak (30mV), the membrane voltage and recovery variable,
if v > = 30mV then
v <--- c,
u <--- u + d
"""
"""
PARAMETERS OF THE MODEL:

By changing the parameters a, b, c, d different ignition patterns can be simulated.
Each parameter corresponds to different aspects of neural behavior.

a. Parameter a describes the time scale of the recovery variable (u recovery variable)
Smaller values result in slower recovery time.

b. Sub-threshold membrane potential of parameter b recovery variable
explains its sensitivity to fluctuations v.

NS. Parameter c describes the post-spike reset value of the membrane potential
K^+ conductivities due to v fast high threshold.

d. Parameter d describes the spike reset of the recovery variable.
u, Na^+ and K^+ conductivities due to slow high threshold.
"""

"""
MODEL INPUT
For simplicity, input to the model (I(t)), 0mV between 0ms and 300ms, followed by 300ms and 1000ms
It is a step function of up to 5 mV between
"""

import numpy as np
import sys
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib.pyplot as plt

h =0.5 # step size
input_onset=300 # step start
input_amp=5 # amplitude of my step

time = np.arange(0,1000.1,h) # time period 1000ms(1sec)

def Input(input_onset,input_amp):
  I=np.zeros((len(time)))    # stream(input)
  for k in range(0,len(time)):
    if time[k]>input_onset:
      I[k]=input_amp  # input change
  return I 

# plotting the input
fig,ax1=plt.subplots(figsize=(12,3))
ax1.plot(time,Input(input_onset,input_amp),'b-') # y tag
ax1.set_xlabel('time(s)')  # x tag

# Make y-axis label, ticks and tick labels match line color.
ax1.set_ylabel('Input mV', color='b')
ax1.set_ylim(0,input_amp*2) # set drawing spacing
plt.title('Figure 2: Input to the system')
plt.show()

# NUMERICAL SOLUTION TO IZHIKEVICH MODEL

def Discrete_Model(a,b,u,v,I):
  v=v+h*(0.04*v*v+5*v+140-u+I) # discrete membrane potential form neuron
  u=u+h*(a*(b*v-u))            # discrete form in membrane recovery variable
  return u,v

# is the main python function. function corresponding to parameters in the model of the same namesake
# takes four variables a,b,c,d.
def Izhikevich(a,b,c,d):
  v=-65*np.ones((len(time))) # sets the initial values of the membrane potential.
  u=0*np.ones((len(time)))   # sets the membrane recovery initial values.
  u[0]=b*v[0]                # initial state

  spiketime=[]
  fired=[]
  I=Input(input_onset,input_amp)
  
  # EULER METHOD
  for k in range(0,len(time)-1):
    u[k+1],v[k+1]=Discrete_Model(a,b,u[k],v[k],I[k])
    if v[k+1]>30:
      v[k+1]=c 
      u[k+1]=u[k+1]+d
  plot_input_output(time,v,I,a,b,c,d)

# RESULT CODE:
# IZHIKEVICH model has drawing function for input(I) and output(v).
# The function takes time, output(v), input(I) and 4 variables a,b,c,d corresponding to the parameters in the pattern of the same letters.
def plot_input_output(time,v,I,a,b,c,d):
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
  plt.show()

Izhikevich(0.02,0.2,-65,8) # RS

Izhikevich(0.1,0.2,-65,2) # FS

Izhikevich(0.02,0.2,-55,4) # IB

Izhikevich(0.02,0.2,-50,2) # CH

Izhikevich(0.02,0.25,-65,0.05) # TC

Izhikevich(0.1,0.26,-65,2) # RZ

Izhikevich(0.02,0.25,-65,2) # LTS


