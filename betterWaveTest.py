import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import wave

# constants
CHUNK = 1024             # samples per frame
update_interval = 0.2    #Use ssh to control or potentiometer

p = pyaudio.PyAudio() #Instancing pyaudio object

fileName = input("File name plz:\n")

raw = wave.open("E:\Code\Code_projects\{file}.wav".format(file = fileName), 'r')
raw2 = wave.open("E:\Code\Code_projects\{file}.wav".format(file = fileName), 'r') #I don't know why I need to open the file twice, don't ask me
stream = p.open(format = p.get_format_from_width(raw.getsampwidth()), channels = raw.getnchannels(), rate = raw.getframerate(), output = True) #Open py audio stream

signal = raw2.readframes(-1)
signal = np.frombuffer(signal, dtype ="int16") #data about the full song

signal = signal / 100 #Unga Bunga moment

#"My waveform is a a wall" mode

# signal2 = np.array([])
# for i in signal:
#     if i > 100:
#         np.append(signal2, i * 10)
#     else:
#         np.append(signal2, i / 10)
#audio_length = round((len(signal) / raw2.getframerate()) / 2) #Can be used for the graph labels
  
duration = np.linspace( #Creates a list of points showing when each sound from signal is played. It's a timeline
        0, # start
        len(signal) / raw2.getframerate(),
        num = len(signal)
    )
  
# Graph code for testing, uncomment if you want
plt.figure(1)
plt.title("Sound Wave")
plt.xlabel("Time")
plt.ylabel("Volume")     
plt.plot(duration, signal)
plt.ion()
plt.show()
plt.pause(0.1)

# Change sound volume into RGB brightness
j = 0 #Counter
color_flags = [] #List containing all the colors
factor = (np.amax(signal) / 510) #There used to be a method behind this, I just found a formula that works alright
for i in duration:
    if signal[j] > 0:
        color_flags.append((signal[j] / factor)) #Translate volume into RGB brightness
    else:
        if j > 0:
            color_flags.append(color_flags[j-1])
        else:
            color_flags.append(0)
    j += 1

# Compress the list as to not kill all the epileptics in the room
compressed_color = [] #The list itself
color_buffer = 0 #Stores color before compression
j = 0 #Counter
timer = update_interval #Used to compress points in specific intervals of time
flag_counter = 0 #Counts how many points were put into the color buffer
for i in color_flags:
    if duration[j] >= timer:
        timer += update_interval
        compressed_color.append([round(color_buffer / flag_counter), duration[j]])
        flag_counter = 0
        color_buffer = 0
    else:
        flag_counter += 1
        color_buffer += i
    j += 1

print(compressed_color) #Testing
print('stream started')

# Read a chunk prior to starting
data = raw.readframes(CHUNK)
j = 0 #Counter
color = 0 #Color to be shown 
start = time.time() #Program needs time to know what time it started at

#I went through all of that trouble so that the computer doesn't have to compute much of anything when actually playing the song
#Play stream (looping from beginning of file to the end)
while data != '':
    # writing to the stream is what *actually* plays the sound
    stream.write(data)
    data = raw.readframes(CHUNK)
    
    if time.time() - start >= compressed_color[j][1]: #Check if program reached one of the "flags" to change color
        color = compressed_color[j][0]
        print(color)
        if len(compressed_color) > j + 1:
            j += 1
        

# cleanup stuff
stream.close()    
p.terminate()