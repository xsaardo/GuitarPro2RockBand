# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 16:49:50 2016

@author: xsaardo
"""

import guitarpro as gp
from matplotlib import pyplot as plt
import numpy as np

from tkFileDialog import askopenfilename

def mapNotes(notes,mappingList):
    for mapping in mappingList:    
        notes = [[mapping[1] if note == mapping[0] else note for note in noteCluster] for noteCluster in notes]
    return notes

def getUniqueNotes(notes):
    notes = sum(notes,[])
    return set(notes)

def getMapping(unique_notes):
    mappingList = []
    for notes in unique_notes:
        drum = raw_input('Map ' + str(notes) + ' to: ')
        mappingList.append((notes,drum))
    return mappingList
        
    
def generateTab(notes,noteTime):
    plt.figure(figsize=(.7,30))
    [plt.hlines(noteTime[ind-1],0,0.75) for ind, x in enumerate(notes) if 'k' in x]
    [plt.plot(0,noteTime[ind-1],'ro') for ind, x in enumerate(notes) if 's' in x]
    [plt.plot(.25,noteTime[ind-1],'yo') for ind, x in enumerate(notes) if 'h' in x]
    [plt.plot(.5,noteTime[ind-1],'bx') for ind, x in enumerate(notes) if 'r' in x]
    [plt.plot(.5,noteTime[ind-1],'bo') for ind, x in enumerate(notes) if 't' in x]
    [plt.plot(0.75,noteTime[ind-1],'go') for ind, x in enumerate(notes) if 'c' in x]
    plt.show()
    
class parsedGPFile(object):
    noteDuration = [];
    notes = [];

    def __init__(self,filename):
        self.notes = []
        self.noteTime = []

        song = gp.parse(filename)

        # Find which track is percussion track
        for track in song.tracks:
            if track.isPercussionTrack:
                drumTrack = track
        
        numMeasures = len(drumTrack.measures)
        measures = drumTrack.measures
        
        noteDuration = []        
        
        for i in range(0,numMeasures):
            beats = measures[i].voices[0].beats
            numBeats = len(beats)
            for j in range(0,numBeats):
                #print 1/beats[j].duration.value
                noteDuration.append(1.0/beats[j].duration.value)
                if len(beats[j].notes) == 0:
                    self.notes.append([0])
                else:
                    noteCluster = []
                    for k in range(0,len(beats[j].notes)):
                        #print beats[j].notes[k].value
                        noteCluster.append(beats[j].notes[k].value)
                    self.notes.append(noteCluster)
        
        self.noteTime = np.cumsum(noteDuration)
 
filename = 'Blink 182 - First Date (Pro).gp3'
fixme = parsedGPFile(filename)
uniqueNotes = getUniqueNotes(fixme.notes)
mappingList = getMapping(uniqueNotes)
notes = mapNotes(fixme.notes,mappingList)
generateTab(notes,fixme.noteTime)

        
'''
print dir(song.tracks[1])
print dir(song.tracks[1].measures[0].voices[0].beats[0].notes)
print song.tracks[1].measures[0].track
print song.tracks[1].measures[1].voices[0].beats[0].notes[1].value
'''