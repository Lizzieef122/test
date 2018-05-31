# -*- coding: utf-8 -*-
"""
Created on Tue May 22 14:15:53 2018

@author: exf266
"""



import dill

import numpy as np


try:
    type(rats)
    print('Using existing data')
except NameError:
    print('Loading in data from pickled file')
    try:
        pickle_in = open('//Users/d1795711/anaconda3/rats.pickle', 'rb')
    except:
        pickle_in = open('//Users/d1795711/anaconda3/rats.pickle', 'rb')
    rats = dill.load(pickle_in)
    
x = rats['PPP1.3'].sessions['s16']  
video_path = 'E:/PPP1-171017-081744_Eelke-171110-104920_Cam1.avi'

import moviepy.editor as mv
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt

##########

def snipper(data, timelock, fs = 1, t2sMap = [], preTrial=10, trialLength=30,
                 adjustBaseline = True,
                 bins = 0):

    if len(timelock) == 0:
        print('No events to analyse! Quitting function.')
        raise Exception('no events')
    nSnips = len(timelock)
    pps = int(fs) # points per sample
    pre = int(preTrial*pps) 
#    preABS = preTrial
    length = int(trialLength*pps)
# converts events into sample numbers
    event=[]
    if len(t2sMap) > 1:
        for x in timelock:
            event.append(np.searchsorted(t2sMap, x, side="left"))
    else:
        event = [x*fs for x in timelock]

    avgBaseline = []
    snips = np.empty([nSnips,length])

    for i, x in enumerate(event):
        start = int(x) - pre
        avgBaseline.append(np.mean(data[start : start + pre]))
#        print(x)
        try:
            snips[i] = data[start : start+length]
        except ValueError: # Deals with recording arrays that do not have a full final trial
            snips = snips[:-1]
            avgBaseline = avgBaseline[:-1]
            nSnips = nSnips-1

    if adjustBaseline == True:
        snips = np.subtract(snips.transpose(), avgBaseline).transpose()
        snips = np.divide(snips.transpose(), avgBaseline).transpose()

    if bins > 0:
        if length % bins != 0:
            snips = snips[:,:-(length % bins)]
        totaltime = snips.shape[1] / int(fs)
        snips = np.mean(snips.reshape(nSnips,bins,-1), axis=2)
        pps = bins/totaltime
              
    return snips, pps

#########

def nearestevents(timelock, events, preTrial=10, trialLength=30):
#    try:
#        nTrials = len(timelock)
#    except TypeError:
#        nTrials = 1
    data = []
    start = [x - preTrial for x in timelock]
    end = [x + trialLength for x in start]
    for start, end in zip(start, end):
        data.append([x for x in events if (x > start) & (x < end)])
    for i, x in enumerate(data):
        data[i] = x - timelock[i]      
    
    return data

##########



def makevideoclip(videofile, event, data, pre=10, length=30, savefile='output.mp4'):
    vidclip = mv.VideoFileClip(videofile).subclip(event-pre,event-pre+length)
    
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    animation = mv.VideoClip(make_frame(ax), duration=length)

    combinedclip = mv.clips_array([[vidclip, animation]])
    combinedclip.write_videofile(savefile, fps=10)

    return combinedclip

def make_frame(t):
    axislimits, rasterlimits = setfiglims(data)
    
    ax.clear()        
    ax.plot(dataUV[:t*(len(dataUV)/duration)], lw=2, color='grey')
    ax.plot(data[:t*(len(data)/duration)], lw=2, color='white')
    
    ax.vlines([val for val in lickdata if val < t*(len(data)/duration)], rasterlimits[0], rasterlimits[1], color='white', lw=1)
    
    ax.set_xlim(0, len(data))
    ax.set_ylim(axislimits[0], axislimits[1])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.text(0, rasterlimits[0], 'licks', fontsize=14, color='w')
    
    return mplfig_to_npimage(fig)

def setfiglims(data):
    datarange = np.max(data) - np.min(data)
    axislimits = [np.min(data), np.max(data)+datarange*0.15]
    rasterlimits = [np.max(data)+datarange*0.05, np.max(data)+datarange*0.15]
      
    return axislimits, rasterlimits

#Code to choose parameters for video
bins = 600
preTrial=10
trialLength=35

#lizzie added bits

def nearestevents(timelock, events, preTrial=10, trialLength=30):
#    try:
#        nTrials = len(timelock)
#    except TypeError:
#        nTrials = 1
    data = []
    start = [x - preTrial for x in timelock]
    end = [x + trialLength for x in start]
    for start, end in zip(start, end):
        data.append([x for x in events if (x > start) & (x < end)])
    for i, x in enumerate(data):
        data[i] = x - timelock[i]      
    
    return data

def snipper(data, timelock, fs = 1, t2sMap = [], preTrial=10, trialLength=30,
                 adjustBaseline = True,
                 bins = 0):

    if len(timelock) == 0:
        print('No events to analyse! Quitting function.')
        raise Exception('no events')
    nSnips = len(timelock)
    pps = int(fs) # points per sample
    pre = int(preTrial*pps) 
#    preABS = preTrial
    length = int(trialLength*pps)
# converts events into sample numbers
    event=[]
    if len(t2sMap) > 1:
        for x in timelock:
            event.append(np.searchsorted(t2sMap, x, side="left"))
    else:
        event = [x*fs for x in timelock]

    avgBaseline = []
    snips = np.empty([nSnips,length])

    for i, x in enumerate(event):
        start = int(x) - pre
        avgBaseline.append(np.mean(data[start : start + pre]))
#        print(x)
        try:
            snips[i] = data[start : start+length]
        except ValueError: # Deals with recording arrays that do not have a full final trial
            snips = snips[:-1]
            avgBaseline = avgBaseline[:-1]
            nSnips = nSnips-1





# Code to choose rat/session and events
x = rats['PPP1.7'].sessions['s10']
all_events = x.left['sipper']
videofile = 'C:\\Users\\jaimeHP\\Downloads\\PPP1-171017-081744_Eelke-171027-111329_Cam2.avi'
all_data = snipper((x.data, x.left['sipper'], t2sMap=x.t2sMap, preTrial=preTrial, trialLength=trialLength, bins=bins)
all_licks = np.concatenate((x.left['lickdata']['licks'], x.right['lickdata']['licks']), axis=0)

event_number=1
event = all_events[event_number]
data = all_data['blue'][event_number][:]
dataUV = all_data['uv'][event_number][:]

lickdatabytrial = nearestevents(all_events, all_licks)
lickdata = lickdatabytrial[event_number]
lickdata = (lickdata+preTrial)*bins/trialLength # scales to match bin number

savefile = 'R:\\DA_and_Reward\\es334\\PPP1\\video\\newcombined-' + str(event_number) + '.mp4'
