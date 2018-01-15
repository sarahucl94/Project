‘’’Author: Sarah Aliko. This code modifies the text file containing subtitles and timings of subtitles obtained online. Then the timings are grouped into pairs (in the format start:end), but rather than use the start:end of subtitles, it uses the inter-subtitle timings to estimate DVS timings. Then it accesses the audio file of the movie (mono audio channel) and splits the DVS timings out of the audio, merging them into a new audio file in “.wav” format.’’’

#Open subtitle file – contains both timings and text
#open new text file to write timings of subs only and remove text
with open("/Volumes/Macintosh HD/Users/sarah/Downloads/subs_timings.txt", "r+") as file:
    with open("/Volumes/Macintosh HD/Users/sarah/Downloads/subs_part3_times.txt", "w+") as a:
        for line in file.read().split():
            result = ''.join(i for i in line if i.isdigit() or i== ':' or i=='.')
            new_list = [result]
            a.write(repr(new_list))
    a.close()


#modify subtitle file to adapt format for analysis
#removes characters that are not timings (eg. commas, dots, brakets)
def new():
    with open("/Volumes/Macintosh HD/Users/sarah/Downloads/subs_part3_times.txt", "r+") as a:
        for line in a.read().split():
            timings = ''.join(i for i in line if not i==']' or not i=="'" or not i=='[')
            timings = timings.replace("['']", '')
            timings = timings.replace('[', '\n')
            timings = timings.replace(']', ' ')
            timings = timings.replace("'", ' ')
            timings = timings.replace(". ", ' ')
            timings = timings.replace("..", ' ')
            timings = timings.replace("::", ' ')
            timings = timings.replace(": ", ' ')


    with open("/Volumes/Macintosh HD/Users/sarah/Downloads/subs_part3_times.txt", "w+") as a:
        a.write(timings)
        a.close()
new()


#open audio file for the movie- has to be in mono audio channel
#if audio channel is not originally mono, modify it using ffmpeg command
#in the terminal.

import numpy as np
import scipy.io.wavfile
fs1, y1 = scipy.io.wavfile.read('/Volumes/Macintosh HD/Users/sarah/Downloads/audio_mono.wav')


time_str = open('/Volumes/Macintosh HD/Users/sarah/Downloads/subs_part3_times.txt').read().replace(' ', "").split(',')



#write the timings as seconds instead of hh:mm:ss format
#select the inter-subtitle timings (ie the ones that should have DVS audio)
def obtain_sec(time_str):
    lst=[]
    subs=[]
    for element in time_str:
        lst.append(element)
    time2 = [i.split() for i in lst]
    flat_time = [item for sublist in time2 for item in sublist if item is not '.']
    for timing in flat_time:
        c = int(timing[0:2]) * 3600 + int(timing[3:5]) * 60 + float(timing[6:11])
        subs.append(c)
        bits = [subs[x:x + 2] for x in range(1, len(subs), 3)]
    return (bits)




#split audio file based on timings above and merge them into new audio file
subtitles = obtain_sec(time_str)
l1 = np.array(subtitles)
l1 = np.ceil(l1*fs1)
newWavFileAsList = []
for elem in l1:
    startRead = elem[0]
    endRead = elem[1]
    if startRead >= y1.shape[0]:
      startRead = y1.shape[0]-1
    if endRead >= y1.shape[0]:
      endRead = y1.shape[0]-1
    newWavFileAsList.extend(y1[int(startRead):int(endRead)])


newWavFile = np.array(newWavFileAsList)
scipy.io.wavfile.write("/Volumes/Macintosh HD/Users/sarah/Downloads/dvs_audio_only.wav", fs1, newWavFile)
