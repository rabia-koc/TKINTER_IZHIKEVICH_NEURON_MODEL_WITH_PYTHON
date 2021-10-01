# The project was implemented with the Python programming language Izhikevich Neuron Model, which provides a real-time audio response to the input audio signal.
# This system processes the input audio signal and transfers it to the Izhikevich Neuron Model algorithm and simultaneously responds with the input audio signal.
import pyaudio
import numpy as np
from scipy import signal
from multiprocessing import Process, Queue
from threading import Thread
import matplotlib.pyplot as plt
import time

winSize = 10   # time the CHUNK
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
h = 0.2
# Values of 10 as the window size and 1024 as the number of continuously changing samples are given.
# The audio signal was recorded in float32 and worked on a single channel.
# The number of samples per second is set to 44100.
# A value of 0.2 is defined for subsampling and the Izhikevich algorithm.

# The processor is the processor that performs the actions that start and finish the algorithm. Two operations were performed within a single processor.
# One of these two actions continuously records the sound from the microphone, the other processes the last 1024 samples and transmits it to the speaker as an Izhikevich response.
# To minimize the latency that may occur, these two separate operations were performed on the same processor and the refresh frequency was set to 1024 (optimal value).
# 1024 new incoming samples were added in succession continuously and used in the audio signal processing algorithm to process it.
# By converting numeric values to "byte" size, I got the output.

# I recorded continuous audio with the callback function.
# Values retrieved in float32 are given as 'in_data' (input data).
# As 'out_data' (output data), the converted values in bytes of the Izhikevich response, or the byte equivalent of 0, are given on a case-by-case basis whether the 'izi2record' queue is empty.
# Thus, I performed audio recording and audio output.

def recordd(record2soundprocess, izi2record):
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        # to process
        incoming = np.frombuffer(in_data, np.float32);
        record2soundprocess.put(incoming)

        # From izi
        if izi2record.empty():
            out_data = np.zeros(np.shape(incoming)).tobytes();
        else:
            incoming = izi2record.get()
            out_data = incoming.tobytes();

        return (out_data, pyaudio.paContinue)

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        pass


# While the audio recording and vocalization process is done by the processor, the 2nd processor passes the raw audio data packets through the signal processing stages with 1024 samples added one after the other.
# First of all, by taking the absolute value of the raw audio data and optimizing the fluctuations in the signal, no data loss was experienced.
# I then removed background noise from the full wave rectified audio signal by equating values less than 0.3 to 0.
# By clearing the signal from background noise, I made it possible to distinguish between foreground sounds and got rid of unnecessary data.
# I got the amplitude envelope of the signal using the hilbert transform (scipy.signal.hilbert) which includes the Fourier transform.
# By removing the envelope of the signal, the high frequency signals were removed and the low frequency signals were retained.
# After going through the raw audio signal processing stages, I transferred it to the model by subsampling.
# In the sub-sampling process, 1024 samples were taken and the sound data, which was renewed and became continuous, was transferred to the model by downloading 116 samples.

def soundprocess(record2soundprocess, record2show, soundprocess2show, soundprocess2izi):
    old_voice = np.zeros(winSize * CHUNK)
    while True:
        if not record2soundprocess.empty():
            yeni_ses = record2soundprocess.get()

            old_voice = np.append(old_voice[-(winSize - 1) * CHUNK:], yeni_ses)
            old_voice = np.abs(old_voice)
            thr = 0.2
            i_clr = np.where(old_voice < thr)
            old_voice[i_clr] = 0;
            sound_hilbert = signal.hilbert(old_voice)
            envelope = np.abs(sound_hilbert)
            envelope = signal.convolve(envelope, np.ones(21), mode='same')

            record2show.put(old_voice)
            soundprocess2show.put(envelope)
            q = envelope[-CHUNK:]
            soundprocess2izi.put(signal.resample(q, 232))


def IZI(soundprocess2izi, izi2record):
    while True:
        while soundprocess2izi.empty():
            pass

        def Discrete_Model(a, b, u, v, I):
            v = v + h * (0.04 * v * v + 5 * v + 140 - u + I)
            u = u + h * (a * (b * v - u))
            return u, v

        def Izhikevich(a, b, c, d):
            v = -65 * np.ones(232)
            u = 0 * np.ones(232)
            u[0] = b * v[0]
            I = soundprocess2izi.get()


            for k in range(0, 116 - 1):
                u[k + 1], v[k + 1] = Discrete_Model(a, b, u[k], v[k], I[k])
                if v[k + 1] > 30:
                    u[k + 1] = u[k + 1] + d
                    v[k + 1] = c
            izi2record.put(signal.resample(v, 1024))

        #Izhikevich(0.02, 0.2, -55, 4)   # Intrinsically Bursting (IB)
        #Izhikevich(0.02, 0.2, -65, 8)  # Regular Spiking (RS)
        Izhikevich(0.1, 0.2, -65, 2)     # Fast Spiking (FS)

# In this code snippet, I introduced the Izhikevich neuron model.
# Mathematical equations are coded. The membrane potential variable and the membrane recovery variable were expressed in terms.
# The data making up the response was oversampled to generate an audio output.
# The code is completed by giving Fast Spiking parameters.

if __name__ == '__main__':
    record2soundprocess = Queue()
    record2show = Queue()
    soundprocess2izi = Queue()
    soundprocess2show = Queue()
    izi2record = Queue()

    fig, ax = plt.subplots(figsize=(15, 8))
    lineSes, = plt.plot(np.zeros(winSize * CHUNK), '-b')
    lineZarf, = plt.plot(np.zeros(winSize * CHUNK), '-r')

    ax.set_ylim(bottom=-1, top=1)

    p1 = Process(target=recordd, args=(record2soundprocess, izi2record))
    p2 = Process(target=soundprocess, args=(record2soundprocess, record2show, soundprocess2show, soundprocess2izi))
    p3 = Process(target=IZI, args=(soundprocess2izi, izi2record))
    p1.start()
    p2.start()
    p3.start()

    time.sleep(2)

    t0 = time.time()
    while (time.time() - t0) < 30:
        time.sleep(0.1)
        if not (record2show.empty() and soundprocess2show.empty()):
            ses = record2show.get()
            zarf = soundprocess2show.get()

            lineSes.set_ydata(ses)
            lineZarf.set_ydata(zarf)


            fig.canvas.draw()
            fig.canvas.flush_events()
    p1.terminate()
    p2.terminate()
    p3.terminate()
    time.sleep(1)

# In this part, which looks like the last part of the code but is actually the beginning, the data coming from the microphone is collected in one place and the processes are connected.
# Commands are given for visualization and 3 operations are defined.
# The first of these processes records the sound from the microphone and responds through the speaker, the other processes 1024 samples.
# The resulting processor generates the Izhikevich response.