try:
    from playsound import playsound
    import pyaudio
    import numpy as np
    
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import seaborn as sns
except:
    print ("Something didn't import")

i=0
k=0
f,ax = plt.subplots(2)
g,bx=plt.subplots(1)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")




li3,=bx.plot(x,y)
bx.set_xlim(0,600)
bx.set_ylim(-40000,40000)
bx.set_title("amplitude graph")


# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 1024 # 1024bytes of data red from a buffer
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "AK.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True)#,
                    #frames_per_buffer=CHUNK)

global keep_going
keep_going = True


def plot_data(in_data):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
    
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = (np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] 

    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    print ("audio values\n",audio_data[0:10])
    print ("normalised amplitude values\n",dfft[0:10])
    
    
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    
    
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)
    
    
    li3.set_xdata(np.arange(len(freq)))
    li3.set_ydata(fft)
    
    #count1=0
    q=0
    p=10
    count1=0
    n=0
    m=10

    for (i,k) in zip(dfft[q:p],freq):
        if i>50.0 and k> 120.0:
            count1=count1+1
            print('c1:',count1)
            q=p   #change this since value is executed only after if condition
            p=p+10

             
    if count1>=7:
        print("\n\n")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("aggressive")
        playsound(r'C:\Users\Ajin George\Desktop\Anjali\a.wav')
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n\n")
    


    # Show the updated plot, but without blocking
    plt.pause(0.01)
    if keep_going:
        return True
    else:
        return False

# Open the connection and start streaming the data
stream.start_stream()
print ("\n+---------------------------------+")
print ("| Press Ctrl+C to Break Recording |")
print ("+---------------------------------+\n")

# Loop so program doesn't end while the stream callback's
# itself for new data
while keep_going:
    try:
        plot_data(stream.read(CHUNK))
    except KeyboardInterrupt:
        keep_going=False
    except:
        pass

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()
