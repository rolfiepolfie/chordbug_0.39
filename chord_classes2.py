# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 06:19:09 2022

@author: rolfe
"""


from dataclasses import dataclass
import time
#from sessionclass import SessionMain


class UserInteraction:
    
    def askuseropenports(rv, midi, filt, ports):
        
        print("***")

        print("open inport for bass: ")
        #if ans == 'y':
        ports.openInport_bass(rv.in_index_bass) 
        midi.setinPort_bass(ports._inPort_bass, ports._inPort_bass_name, filt.trigBass) 
        time.sleep(1)
        
         
        print("***")
        print("open inport for control1: ")

        
        ports.openInport_control(rv.in_index_control1) 
        midi.setinPort_controlButtons(ports._inPort_control, ports._inPort_control_name, filt.trigControlChord) 
        time.sleep(1)
        
        print("open inport for control2: ")
        
        if rv.in_index_control2 != -1: 
        
            ports.openInport_control(rv.in_index_control2) 
            midi.setinPort_controlButtons(ports._inPort_control, ports._inPort_control_name, filt.trigControlChord) 
        
        else:
            print("NB ** port not opened **")
                    
        
        time.sleep(1)
        print("***")
   
    
   
    
    def readportnumbers():
        
        @dataclass
        class Returnvalue:
            out_index:          int
            in_index_bass:      int
            in_index_control1:  int
            in_index_control2:  int
            
        while True: # read in a midi port device 
            try:
                print(" *********** -1 if this service is not wanted. ************* ")
                print(" - ")
                out_index = int(input("For chord output, enter a number (default 0): ") or "0")
                print('\n')
                
                in_index_bass = int(input("For bass input, enter a number(default 1): ") or "1") #1
                      
                in_index_control1 = int(input("For control input1, enter a number(default 0): ") or "0") #3
                in_index_control2 = int(input("For control input2, enter a number(default -1): ") or "-1") #0
                
                break
            
            except Exception as e:
                print("er, ror: " + str(e))
                
        return Returnvalue(out_index, in_index_bass, in_index_control1, in_index_control2)
          



def scan(msgtype, note_cc, Globals, msg, callback, extraparams=None):
    """
    A helper function called by callbackChord_Control_Buttons(...)
    
    Scanning to se if a midi message match anything in the global lists: 
        chords = [] 
        controls = []
    If so, the _callback_scan() is invoked.
    msgtype: the type midi message cousing the triggering is a list [.....]
    note_cc: the midi note or CC (control change) causing the triggering
    callback: the function to be evoked if all parameters match 
    
    """
    '''
    the returnvalue from this function is actually the return from _callback_scan(...)
    '''
               
    for control in Globals.controls:
        if msgtype in control.msgtype: 
            if note_cc in control.note_cc:
                return callback(control, msgtype, note_cc, msg) #returns class instance
                
    

class Filter:
    '''
    1. Mido system first calls these functions in __init__  parameter
    2. Functions are then filtered dependent on their parameter 
    3. These function is then called and indicated with an _
    
    This filter handles Midi input only
    This filter only trigger callbacks with 
    midi messages with the correct channel property value
    

    '''    
    def __init__(self, callback_bass, callback_controlchord): 
        
        self._cbBass=callback_bass
        self._cb_controlchord=callback_controlchord
    
        self._basschannel=0
        self._controlChordChannel=0

        self._activated=False
        
        
    def activate(self):
        self._activated=True
    
    def deactivate(self):
        self._activated=False
        
    
    def filteroutBass(MidimsgTypes):
        '''
        Messages are removed, but messages with correct channel is triggered
        add an array or class properties woth datatyps to ignore 
        in the message stream 
        '''
        pass
    
    
    def filteroutControlChord(MidimsgTypes):
        '''
        add an array or class properties woth datatyps to ignore 
        in the message stream 
        '''
        pass
    
    def report(self):
        '''
        prints a small report listing the filters attributes 
        
        '''        
        print('\n')
        print('--- Midi Filter Report ---')
        print("Midi channel bass: ", self._basschannel)
        print("Midi channel control: ", self._controlChordChannel)
        
        if self._activated:
            print("* filter  is activated ---")
        else:
            print("* filter NOT activated ---")
            
        
        
    def _setmidichannelBass(self, channel):
        self._basschannel=channel
        #print('Filter midichannel bass set: ', channel)
    
    def getMidiChBass(self):
        return self._basschannel
    
    def getMidiChCtrlChord(self):
        return self._controlChordChannel
        
    def _setmidichannelChordControl(self, channel):
        self._controlChordChannel=channel
        #print('Filter control-chord midi channel bass set: ', channel)
    
    def setAllMidiChannels(self, session):
        self._basschannel=session.midichannelBass
        self._controlChordChannel=session.midiChannelControls
        

        
    
    def _onlychannelmessages(self, msg):
        try:
            msg.channel #access attribute to check 
            return True
        except AttributeError:
            return False

    #This trigs the callback for bass 
    def trigBass(self, msg):
        # returns true of message contains channel property
        # here we filter out and make sure all messages 
        # triggered got a channel property
        #print('filter - trigBass: ', msg)
        
        #if filter is deactivated we call the callback anyway and escape
        if self._activated == False: 
            self._cbBass(msg) #calling callback function
            return
        
        
        if not self._onlychannelmessages(msg): 
            print("non cannel msg ignored: ", msg)
            return 
                
        if msg.channel == self._basschannel: 
            self._cbBass(msg) #calling callback function
            return
            
     #This trigs the callback for control and chord        
    def trigControlChord(self, msg):
        #print('filter - trigControlChord: ', msg)
        
        #if filter is deactivated we call the callback anyway and escape
        if self._activated == False: 
            self._cb_controlchord(msg) #calling callback function
            return
            
        if not self._onlychannelmessages(msg): 
            print("non channel msg ignored ", msg)
            return 
        
        if msg.channel == self._controlChordChannel: 
            self._cb_controlchord(msg) #calling callback function
            return
    
 ### messages triggered always have the channel property   
 

class CCvalues:
    """
    defines values that follows a CC (Control Change) message (CC, value)
    """
    ALL_SOUND_OFF = 120 #check midi spec for this one 
    RESET_ALL_CONTROLLERS = 121
    ALL_NOTES_OFF = 123
   
    # 122 Local Control On/Off  -  interrupt the internal control path between the keyboard and the sound-generating circuitry
    # 123 All Notes Off
    # 124 Omni Mode Off
    # 125 Omni Mode On
    # 126 Poly Mode On/Off
    # 127 Poly Mode Mono Off

    #https://www.lim.di.unimi.it/IEEE/MIDI/SOT0.HTM#Local

class utils:
    def availableCC():
        s="""
        These is free to use Control Change Messages ...
        """
        print(s)
        print("CC 3")
        print("CC 9")
        print("CC 14-15")
        print("CC 20-31")
        print("CC 85-87")
        print("CC 89-90")
        print("CC 102-119")
    
    # def showkeyb():
    #     img = mpimg.imread('keyb.png')
    #     plt.imshow(img)
    #     plt.show()
    









