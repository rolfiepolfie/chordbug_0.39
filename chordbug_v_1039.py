# -*- coding: utf-8 -*- 

import mido as mido
import config ##globals config variables for this app 
from sessionclass import Misc
from chord_classes1 import Chords, MidimsgType, Ports, MidiComm , Midimess
from chord_classes1 import Controls, Control
from chord_classes2 import Filter, scan


from setup import SetupBlacstarController
from sessionclass import SessionMain

from chord_classes2 import UserInteraction as ui
import rtmidi as rt
import sys
import globalvars as glob
import gmsounds as gm
#################################################################################################


def _callback_scan(classinstance, msgtype, note_cc, mess): #class instance , messagetype that triggered 
    '''    
    A helper function for the callback function
    The mess parameter contains all parameters
    This callback scans for Controls
    '''
        
    def iscontrol(instance): return isinstance(instance, Control)
    #def isAnothercontrol(instance): return isinstance(instance, AnotherControl)
        
    def activate_control(args, instance):
        instance.function(args) #every control got a function named 'function'
        
                
    if iscontrol(classinstance): 
        # I pack all sorts of parameters in here 
        # arguments to functions are decided here
        args=glob.Globals, msgtype, note_cc, mess, midi #is all needed? common parameters for all control.function(...)
        activate_control(args, classinstance)
        return classinstance # needed?
    
    
    #future versions
    #if isAnotertypeofControl(classinstance):
    #    pass
    
     
def callback_Control_Buttons(msg):
    '''
    check type of incoming midi-message
    scan for chords and controls giving the scan function the corect midi-messages
    
    the scan() function returns classinstance of the chord/control if needed
    the return of scan() is determined by the return value of _callback_scan()
    with other words: classinstance object
    '''
      
    mess=Midimess(msg)
    
    
    s="Nothing found ! - "
    
    if mess.isnoteOn():       
        r=scan(MidimsgType.note_on, msg.note , glob.Globals, mess, _callback_scan) #fill he globals       
        if r is None: print(s+mess.totext()) 
                    
        #Globals.global_bassdown=False #.....
        return        
        
    
    if mess.isnoteOff():
        r=scan(MidimsgType.note_off, msg.note , glob.Globals, mess, _callback_scan) #fill he globals 
        if r is None: print(s+mess.totext())
        return
    
    
    if mess.isControlChange():
        print("control-changes are not supported!")
        #scan(MidimsgType.controlchange, msg.control ,Globals, mess, _callback_scan)
        return
    
    #include more messages in later editions
    #if mess.isProgramChange():
    #    return
    
    
        
def callbackBass(msg):  #rename msg to midiOriginal    
    ''' 
    msg = original MIDI message, recall only original messages for the engine 
    set flag global_bassdown
    set root-note in global_chord_root
    send bass-note as midi-trough if requested 
    '''
    
    midimsg=Midimess(msg)
    
    print('callbackBass2 - ', msg)
    
    
    def alterOutMidiChannel(newchannel):
        '''
        if you want alter the output midichannel only
        while retaining the other parameters  '''
        midi.sendMessageOut(msg.copy(channel=newchannel))
        

    if session._midiTrough:        #<--- make flag later on 
        midi.sendMessageOut(msg) #mimics the same as midi-through 
        #########print("channel channel bass out: ", midimsg.channel) #############
        #using midimsg did not work ..need original midi message!
        #alterOutMidiChannel(10)
    
    
    if midimsg.isnoteOn():    
        glob.Globals.global_bassdown=True
        
        if glob.Globals.global_Control_disable_chord_root == False: #control = freeze-root
           glob.Globals.global_chord_root=msg.note #we know it is a note at this stage
            
        print("global_chord_root note: ", glob.Globals.global_chord_root)
        return
        
    if midimsg.isnoteOff():
    
        glob.Globals.global_bassdown=False
        #print("Globals.global_bassdown=False")
        return
    

    
# -- global objects, later to be compiled into a session object     
midi = MidiComm(mido, offset=config.__offset__, chordTimeLength=config.__chordTimeLength__) #offset = transpose 
ports = Ports(mido)
session = SessionMain()

#Other objects should ask the filter about the midi-channels?

# filter is calling the callbacks from the parameters in the constructor
# the hardware is  connected  via the filterMidi instance
## recall:  ui.askuseropenports(rv, midi, filterMidi, ports)
# the filter decides if it shall trigger the callbacks 
filterMidi=Filter(callbackBass, callback_Control_Buttons) 


# we will move eberything related to a seesion inside the Session class
#session=Session(mido)  #rename to defualtSession
#session.activateMidiTrough()

class SetupHardware1:
    '''
    This is a PRESET setting up a collection of boxes 
    
    '''    
    #here we decide what arrays tocadd to the Globals.controls array 
    # these arrays are controls that can also be a chord_send_control
    #we use the append command to add several controllers
    
    # notes are: 12, 14, 16, 17, 19, 21 - blackstar controller 1
    
    control1=SetupBlacstarController().getControlArray1(Controls, Chords)
    control2=SetupBlacstarController().getControlArray2(Controls, Chords) #test
    
    #nb! do not use the same notes/cc if using the sme midi-channel    
    # here we put the control-array in series     
    glob.Globals.controls.extend(control1)
    glob.Globals.controls.extend(control2)
    #using extend or append? 
    # or control1 + control2 ?
    
    
    
def Configure():
    
    SetupHardware1()
    
    #midichannels [0...15] 
    session.midichannelBass=12
    session.MidiChannelControls=14
    session.MidiChannelOut=15
    
    session._midiTrough=True
    
    
    #remark Misc = class object not instance
    Misc.functionalityreport(glob.Globals.controls) #report connection between controls - midi.numbers for this session
    
    ports.report_devices()   
    rv=ui.readportnumbers()  #reads port indexes from user
        
    ports.openOutPort(rv.out_index) #usually there is always an outport on a computer
    
    ui.askuseropenports(rv, midi, filterMidi, ports)
    
        
    # bass must +1
    #2,1,16 (in-bass, in-chords, in-controls, out-chords)
    # chords and controls will be merged to in-controls

    def setupFilter(session, filterMidi):
        #filterMidi.setAllMidiChannels(session)
        #filterMidi.setMidiChannels(2, 16, 16, 15) #make this !!!
        filterMidi.deactivate()  # <- remember to activate Filter 
        #filterMidi.report()
    
    def setupMidi(midi, ports, session):
        
        print("*********************************************************")
    
        midi.setOutPort(ports._outPort)       
        midi.setAllMidiChannels(session)  
        midi.sendProgamChange(gm.GmSounds.Celesta)
        midi.sendOutVolume(120)
        midi.testOut() # play 4 tones
        midi.sendOutVolume(0)  #activate live
        midi.testOut() # should be silent 
       
            
    setupFilter(session, filterMidi)
    setupMidi(midi, ports, session)
    
    session.report()
    midi.report()
    filterMidi.report()
    ports.report()  
    
    
def _destruct():
    '''
    This will work as the destructor in the later Session Class 
    '''
    
    #print("- destructor -")
    
    if midi.InportsEmty()== False:
        print('* sending all notes off')
        midi.sendAllNotesOff()

        print('* closing all ports')
        ports.closeAllPorts() 
        
    ports.report()
    print('* program ended - bye')
    Misc.printTitle(mido, rt, sys, config.___version___, config.___title___)
    raise SystemExit(0) #clean way to exit , no traceback


# new idea: make a function: change chord function codepage
# exp: a device get a new selection of chords 2 -3 of them should be enough


'''

        
'''
def main():
    
    
    Misc.printTitle(mido, rt, sys, config.___version___, config.___title___)
    Configure()
    print(" \n NB! if using same midi-channel on both chord+controls")
    print("do not use the same MIDI-notes or CC messages \n")
    
    print("q-quits")
    print("p-panic")
    print("t-test")
    print('n - new page with chordsx|')
    
    midi.startLoop_keyboardlistener(_destruct, midi) # polling the keyboard 
    

##################################################################################   
if __name__ == "__main__": main()    
    
    