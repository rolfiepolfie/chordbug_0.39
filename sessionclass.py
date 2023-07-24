# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 17:51:35 2023

@author: rolfe
"""
  
#from dataclasses import dataclass
from chord_classes1 import Controls, Chords
from chord_classes2 import UserInteraction as ui
import gmsounds as gm

from setup import SetupBlacstarController


class SessionMain():
    
    def __init__(self):
        self._midichannel_bass =0
        self._midiTrough = True
        self._midichannel_out=0
        self._midichannel_controls=0
        
        self._controlArraySession = None
    
    
    
    # @dataclass
    # class data:
    #     '''
    #     data struct used during a typical session
    #     '''
    #     out_port_index: int
    #     in_port_index_bass: int
    #     in_port_index_control: int
      
    #     midi_channel_in_bass: int
    #     midi_channel_in_control: int
       
    #     midi_channel_out: int
       
    #     filepath: str
    #     controlSchemes: int
    
    def listControlsCurrentSession():
        pass
    
    def addChordScheme(controlArr):
        '''
        '''
        
        #controlarray.extend(.....)
        
        pass
    
    def nextChordScheme():
        pass
    
    
    def _attachControlstoGlobal():
        '''
        
        '''
        #Global.controls = self._controlArraySession
        pass
    
    
    
        
    @property
    def midichannelBass(self):
        return self._midichannel_bass
    
    @midichannelBass.setter
    def midichannelBass(self, ch):
        self._midichannel_bass = ch
            
    @property
    def midiChannelControls(self):
        return self._midichannel_controls
    
    @midiChannelControls.setter
    def midiChannelControls(self, ch):
        self._midichannel_controls = ch      
        
    @property
    def midiChannelOut(self):
        return self._midichannel_out
    
    @midiChannelOut.setter
    def midiChannelOut(self, ch):
        self._midichannel_out = ch   
    
    def report(self):
        print('\n')
        print(" --- Session Report --- ")
        print("Midi channel out: \t\t", self._midichannel_out+1)
        print("Midi channel control: \t", self._midichannel_controls+1)
        print("Midi channel bass: \t\t", self._midichannel_bass+1)
        
        print('Midi trough: ', self._midiTrough)
        

        
class Misc():
    
    #change to live session report ...
    def functionalityreport(controls):
        """
        Prints all the chords and controls loaded in this session 
        
        """

        print("\n")
        print("--- CONTROLS registered for controller messages this session ---")
        for c in controls:     
        
            print("\t control name: \t", c.name)   
            print("\t triggered by: \t", c.msgtype)
            print("\t note_cc: \t\t", c.note_cc)
            print("\t action: \t\t", c.action)
            #print("\n")
        
        print("\n")
  
    
    def classname(self): return __class__.__name__
    
    #def isControlChange(msg):
    #    return msg.type == 'control_change'
    
    #def isNote(msg):
    #    return msg.type == 'note_on' or msg.type == 'note_off'
    #    #return msg.type in ('note_on', 'note_off') # alternative
    
    def undefined_CC():
        t1=" Undefined MIDI CC List"

        t2="CC 3 "
        t3="CC 9 "
        t4="CC 14-15 "
        t5="CC 20-31 "
        t6="CC 85-87 "
        t7="CC 89-90 "
        t8="CC 102-119 "
        return t1+t2+t3+t4+t5+t6+t7+t8
        
        
    def listClassMembers(theObject):
        
        for property, value in vars(theObject).items():
            print(property, ":", value)
    
    def printUserprotertiesClass(clas):
        print([ m for m in dir(clas) if not m.startswith('__')])
    
    def clearSpyderTerminal():
        print("\033[H\033[J")  
    

    def printTitle(mido, rt, sys, ver, title): # the app's name .... 
        print("")
        print("*********************************")
        
        #print(' ▄████▄   ██░ ██  ▒█████   ██▀███  ▓█████▄  ██▓ ▄▄▄       ██▓    ')
        #print('▒██▀ ▀█  ▓██░ ██▒▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌▓██▒▒████▄    ▓██▒    ')
        #print('▒▓█    ▄ ▒██▀▀██░▒██░  ██▒▓██ ░▄█ ▒░██   █▌▒██▒▒██  ▀█▄  ▒██░    ')
        #print('▒▓▓▄ ▄██▒░▓█ ░██ ▒██   ██░▒██▀▀█▄  ░▓█▄   ▌░██░░██▄▄▄▄██ ▒██░    ')
        #print('▒ ▓███▀ ░░▓█▒░██▓░ ████▓▒░░██▓ ▒██▒░▒████▓ ░██░ ▓█   ▓██▒░██████▒')
        #print('░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒▓  ▒ ░▓   ▒▒   ▓▒█░░ ▒░▓  ░')
        #print('  ░  ▒    ▒ ░▒░ ░  ░ ▒ ▒░   ░▒ ░ ▒░ ░ ▒  ▒  ▒ ░  ▒   ▒▒ ░░ ░ ▒  ░')

     ### a testing function ... shall be removed and replaced with Chord-Service  
        print("Title: \t\t\t\t" , title)
        print("Python installed: \t", sys.version_info[0],',', sys.version_info[1])
        print("Mido version:   \t", mido.__version__)
        print("Backend version RT:\t", rt.__version__)
        print("Chordial version: \t", ver)
     
     
    def overviewChords():
        return """
                    https://www.pianochord.org/c5.html
            
            C - C major (C△)
            Cm - C minor
            C7 - C dominant seventh
            Cm7 - C minor seventh
            
            Cmaj7 - C major seventh (C△7)
            CmM7 - C minor major seventh
            
            C6 - C major sixth
            Cm6 - C minor sixth
            C6/9 - C sixth/ninth (sixth added ninth)
            
            C5 - C fifth   (interval - 2 notes)
            
            C9 - C dominant ninth
            Cm9 - C minor ninth
            Cmaj9 - C major ninth
            
            C11 - C eleventh
            Cm11 - C minor eleventh
            
            C13 - C thirteenth
            Cm13 - C minor thirteenth
            Cmaj13 - C major thirteenth
            
            Cadd - C add
            C7-5 - C seven minus five
            C7+5 - C seven plus five
            Csus - C suspended
            
            Cdim - C diminished (C°)
            Cdim7 - C diminished seventh (C°7)
            Cm7b5 - C minor seventh flat five (Cø)
            
            Caug - C augmented (C+)
            Caug7 - C augmented seventh
        """


     
     

    