#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.10),
    on Mon Mar  9 13:54:39 2026
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

from psychopy import gui, core
import json

# Choose the language for the experiment
dlg = gui.Dlg(title="Select Language")
dlg.addField("Language:", choices=["English", "French"])
ok_data = dlg.show()
if not dlg.OK:
    core.quit()
language = ok_data[0]

# Import the texts
if language == 'English':
    with open('moose_english.json', 'r', encoding="utf-8") as file:
        dt_txt = json.load(file)
else:
    with open('moose_french.json', 'r', encoding="utf-8") as file:
        dt_txt = json.load(file)





# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.10'
expName = 'moose_adapt'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/etudiant.e.s/Documents/Stim_adapt_SoA/script/moose_adapt_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Initiate"
InitiateClock = core.Clock()
import random
from psychopy import visual
from psychopy import sound



# Hide cursor
win.mouseVisible = False

# preload the .wav file
bellowSound = sound.Sound('bellow50.wav')  

# Prepare the warning text holder
warning_text = visual.TextStim(win, text="", color="white", height=0.8)

# Rescale for MacBook
# Only the mouse position needs to be rescaled. The rest is OK
monitor_pxl_size = win.monitor.getSizePix()
window_pxl_size = win.size
scaling_x = monitor_pxl_size[0]/window_pxl_size[0]
scaling_y = monitor_pxl_size[0]/window_pxl_size[0]

# check window and monitor size (in pixels) and monitor width (in cm)
print("Window size (px):", win.size)
print("Monitor size (px):", win.monitor.getSizePix())
print("Width (cm):", win.monitor.getWidth())

# Define circular area
circle_center = (0,0)  # x,y
circle_radius = 1.85  # cm

# Define distance from center for anticipated below
distance_for_anticipated_below = 2.35 # cm

# Scale
x_min, x_max, y_pos = -10, 10, 0  
scale_line = visual.Line(win, start=(x_min, y_pos), end=(x_max, y_pos), lineWidth=2, units="cm")

# Ticks of the scale
n_ticks = 11  
ticks = []
for i in range(n_ticks):
    x = x_min + i*(x_max-x_min)/(n_ticks-1)
    ticks.append(visual.Line(win, start=(x, y_pos-0.1), end=(x, y_pos+0.1), lineWidth=2))

# Labels of the scale
general_label = visual.TextStim(win, text=dt_txt['text_general_label'],
                              pos=(x_min, y_pos+2.0), height=0.6, anchorHoriz='left', alignText='left')
left_label = visual.TextStim(win, text=dt_txt['text_left_label'], pos=(x_min, y_pos-1), height=0.6, anchorHoriz='left', alignText='left', anchorVert='top')
center_label  = visual.TextStim(win, text=dt_txt['text_center_label'], pos=(0, y_pos-1), height=0.6, alignText='center', anchorVert='top')
right_label = visual.TextStim(win, text=dt_txt['text_right_label'],
                              pos=(x_max, y_pos-1), height=0.6, anchorHoriz='right', alignText='right', anchorVert='top')

# Red cross (invisible before the click)
red_x = visual.TextStim(win, text="X", color="red", height=1, pos=(0, y_pos), opacity=0.0)

# Initialize counter
block_nb = -1
total_trial_nb = 0
this_block_trial_nb = 0
correct_trial_nb = 0

# Initialize components for Routine "Instruc"
InstrucClock = core.Clock()
Insctruction = visual.TextStim(win=win, name='Insctruction',
    text=dt_txt['text_instruction'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()

# Initialize components for Routine "Instruc_train"
Instruc_trainClock = core.Clock()
Instruction_train = visual.TextStim(win=win, name='Instruction_train',
    text=dt_txt['text_instruction_adapt'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_5 = keyboard.Keyboard()

# Initialize components for Routine "Delay_for_adapt"
Delay_for_adaptClock = core.Clock()

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

# Initialize components for Routine "Moose"
MooseClock = core.Clock()
moose = visual.ImageStim(
    win=win,
    name='moose', units='cm', 
    image='moose.png', mask=None,
    ori=0, pos=(0, 0), size=(13.25, 22.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Pause1"
Pause1Clock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text=dt_txt['text_pause'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Pause2"
Pause2Clock = core.Clock()
sound_1 = sound.Sound('A', secs=0.5, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1)

# Initialize components for Routine "Instruc_adapt"
Instruc_adaptClock = core.Clock()
Insctruction_adapt = visual.TextStim(win=win, name='Insctruction_adapt',
    text=dt_txt['text_instruction_adapt'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_2 = keyboard.Keyboard()

# Initialize components for Routine "Delay_for_adapt"
Delay_for_adaptClock = core.Clock()

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

# Initialize components for Routine "Moose"
MooseClock = core.Clock()
moose = visual.ImageStim(
    win=win,
    name='moose', units='cm', 
    image='moose.png', mask=None,
    ori=0, pos=(0, 0), size=(13.25, 22.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Pause1"
Pause1Clock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text=dt_txt['text_pause'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Pause2"
Pause2Clock = core.Clock()
sound_1 = sound.Sound('A', secs=0.5, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1)

# Initialize components for Routine "Instruc_test"
Instruc_testClock = core.Clock()
Instruction_test = visual.TextStim(win=win, name='Instruction_test',
    text=dt_txt['text_instruction_test'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

# Initialize components for Routine "Moose"
MooseClock = core.Clock()
moose = visual.ImageStim(
    win=win,
    name='moose', units='cm', 
    image='moose.png', mask=None,
    ori=0, pos=(0, 0), size=(13.25, 22.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Scale"
ScaleClock = core.Clock()
mouse_scale = event.Mouse(win=win)
x, y = [None, None]
mouse_scale.mouseClock = core.Clock()

# Initialize components for Routine "Pause1"
Pause1Clock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text=dt_txt['text_pause'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Pause2"
Pause2Clock = core.Clock()
sound_1 = sound.Sound('A', secs=0.5, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1)

# Initialize components for Routine "Instruc_adapt"
Instruc_adaptClock = core.Clock()
Insctruction_adapt = visual.TextStim(win=win, name='Insctruction_adapt',
    text=dt_txt['text_instruction_adapt'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_2 = keyboard.Keyboard()

# Initialize components for Routine "Delay_for_adapt"
Delay_for_adaptClock = core.Clock()

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

# Initialize components for Routine "Moose"
MooseClock = core.Clock()
moose = visual.ImageStim(
    win=win,
    name='moose', units='cm', 
    image='moose.png', mask=None,
    ori=0, pos=(0, 0), size=(13.25, 22.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Pause1"
Pause1Clock = core.Clock()
pause_text = visual.TextStim(win=win, name='pause_text',
    text=dt_txt['text_pause'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Pause2"
Pause2Clock = core.Clock()
sound_1 = sound.Sound('A', secs=0.5, stereo=True, hamming=True,
    name='sound_1')
sound_1.setVolume(1)

# Initialize components for Routine "Instruc_test"
Instruc_testClock = core.Clock()
Instruction_test = visual.TextStim(win=win, name='Instruction_test',
    text=dt_txt['text_instruction_test'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_3 = keyboard.Keyboard()

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()

# Initialize components for Routine "Moose"
MooseClock = core.Clock()
moose = visual.ImageStim(
    win=win,
    name='moose', units='cm', 
    image='moose.png', mask=None,
    ori=0, pos=(0, 0), size=(13.25, 22.7),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Scale"
ScaleClock = core.Clock()
mouse_scale = event.Mouse(win=win)
x, y = [None, None]
mouse_scale.mouseClock = core.Clock()

# Initialize components for Routine "Finalize"
FinalizeClock = core.Clock()
GoodBye = visual.TextStim(win=win, name='GoodBye',
    text=dt_txt['text_goodbye'],
    font='Arial',
    pos=(0, 0), height=1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp_4 = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Initiate"-------
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
InitiateComponents = []
for thisComponent in InitiateComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
InitiateClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Initiate"-------
while continueRoutine:
    # get current time
    t = InitiateClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=InitiateClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InitiateComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Initiate"-------
for thisComponent in InitiateComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Hide cursor
win.mouseVisible = False

# the Routine "Initiate" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Instruc"-------
continueRoutine = True
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
InstrucComponents = [Insctruction, key_resp]
for thisComponent in InstrucComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
InstrucClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instruc"-------
while continueRoutine:
    # get current time
    t = InstrucClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=InstrucClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Insctruction* updates
    if Insctruction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Insctruction.frameNStart = frameN  # exact frame index
        Insctruction.tStart = t  # local t and not account for scr refresh
        Insctruction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Insctruction, 'tStartRefresh')  # time at next scr refresh
        Insctruction.setAutoDraw(True)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstrucComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instruc"-------
for thisComponent in InstrucComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instruc" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Instruc_train"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_5.keys = []
key_resp_5.rt = []
_key_resp_5_allKeys = []
# Define the block type, reinitialize counters, increment block number
block_type = 'training'
this_block_trial_nb = 0
correct_trial_nb = 0
block_nb +=1
# keep track of which components have finished
Instruc_trainComponents = [Instruction_train, key_resp_5]
for thisComponent in Instruc_trainComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Instruc_trainClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instruc_train"-------
while continueRoutine:
    # get current time
    t = Instruc_trainClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Instruc_trainClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Instruction_train* updates
    if Instruction_train.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Instruction_train.frameNStart = frameN  # exact frame index
        Instruction_train.tStart = t  # local t and not account for scr refresh
        Instruction_train.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Instruction_train, 'tStartRefresh')  # time at next scr refresh
        Instruction_train.setAutoDraw(True)
    
    # *key_resp_5* updates
    waitOnFlip = False
    if key_resp_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_5.frameNStart = frameN  # exact frame index
        key_resp_5.tStart = t  # local t and not account for scr refresh
        key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
        key_resp_5.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_5.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_5.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_5_allKeys.extend(theseKeys)
        if len(_key_resp_5_allKeys):
            key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
            key_resp_5.rt = _key_resp_5_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instruc_trainComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instruc_train"-------
for thisComponent in Instruc_trainComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instruc_train" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
training_block = data.TrialHandler(nReps=10, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='training_block')
thisExp.addLoop(training_block)  # add the loop to the experiment
thisTraining_block = training_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTraining_block.rgb)
if thisTraining_block != None:
    for paramName in thisTraining_block:
        exec('{} = thisTraining_block[paramName]'.format(paramName))

for thisTraining_block in training_block:
    currentLoop = training_block
    # abbreviate parameter names if possible (e.g. rgb = thisTraining_block.rgb)
    if thisTraining_block != None:
        for paramName in thisTraining_block:
            exec('{} = thisTraining_block[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    correct_trial_training = data.TrialHandler(nReps=99, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='correct_trial_training')
    thisExp.addLoop(correct_trial_training)  # add the loop to the experiment
    thisCorrect_trial_training = correct_trial_training.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_training.rgb)
    if thisCorrect_trial_training != None:
        for paramName in thisCorrect_trial_training:
            exec('{} = thisCorrect_trial_training[paramName]'.format(paramName))
    
    for thisCorrect_trial_training in correct_trial_training:
        currentLoop = correct_trial_training
        # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_training.rgb)
        if thisCorrect_trial_training != None:
            for paramName in thisCorrect_trial_training:
                exec('{} = thisCorrect_trial_training[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Delay_for_adapt"-------
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        Delay_for_adaptComponents = []
        for thisComponent in Delay_for_adaptComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Delay_for_adaptClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Delay_for_adapt"-------
        while continueRoutine:
            # get current time
            t = Delay_for_adaptClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Delay_for_adaptClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            sound_delay = 0.250
            continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Delay_for_adaptComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Delay_for_adapt"-------
        for thisComponent in Delay_for_adaptComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Delay_for_adapt" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Fixation"-------
        continueRoutine = True
        # update component parameters for each repeat
        # Hide cursor
        win.mouseVisible = False
        
        # Fixation cross
        fix_size = 1.6   
        
        # Stimuli
        hor_line = visual.Line(win,  start=(-fix_size, 0), end=(fix_size, 0), lineWidth=5, units="cm")
        ver_line = visual.Line(win,  start=(0, -fix_size), end=(0, fix_size), lineWidth=5, units="cm")
        
        # Start timer
        fixation_timer = core.Clock()
        
        # Enter the counter for this trial
        thisExp.addData('block_nb', block_nb)
        thisExp.addData('total_trial_nb', total_trial_nb)
        thisExp.addData('this_block_trial_nb', this_block_trial_nb)
        thisExp.addData('correct_trial_nb', correct_trial_nb)
        
        # Enter the type of block
        thisExp.addData('block_type', block_type)
        
        # get the absolute time
        thisExp.addData('absolute_time', tThisFlipGlobal)
        
        # keep track of which components have finished
        FixationComponents = []
        for thisComponent in FixationComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        FixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Fixation"-------
        while continueRoutine:
            # get current time
            t = FixationClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=FixationClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            while fixation_timer.getTime() < 0.5:
                hor_line.draw()
                ver_line.draw()
                win.flip()
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Fixation"-------
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Moose"-------
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the mouse
        gotValidClick = False  # until a click is received
        # Set initial position (x, y) in cm
        mouse.setPos((-9.7, 0))
        
        # Show the cursor
        win.mouseVisible = True
        
        # Flags to track trial state
        trial_ended = False
        warning_shown = False
        
        # get the fixation time
        thisExp.addData('fixation_time', fixation_timer.getTime())
        
        # Start timer for 1-second limit
        moose_timer = core.Clock()
        
        # Schedule sound after delay
        # delay_choices = [0.2, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]  # seconds
        # sound_delay = random.choice(delay_choices)
        delay = float(sound_delay)
        if delay < 0:
            condition = 'anticipated'
        else:
            condition = 'delayed'
        
        # The jitter for the disappearance after the beginning of the trial
        jitter = random.randrange(-200, 200)/1000
        
        # Add some scheduled time
        thisExp.addData('scheduled_sound_delay', delay)
        thisExp.addData('scheduled_jitter', jitter)
        # keep track of which components have finished
        MooseComponents = [moose, mouse]
        for thisComponent in MooseComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        MooseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Moose"-------
        while continueRoutine:
            # get current time
            t = MooseClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=MooseClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *moose* updates
            if moose.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                moose.frameNStart = frameN  # exact frame index
                moose.tStart = t  # local t and not account for scr refresh
                moose.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moose, 'tStartRefresh')  # time at next scr refresh
                moose.setAutoDraw(True)
            if not trial_ended:
            
                # Detecting cursor position and click
                x, y = mouse.getPos()
                buttons = mouse.getPressed()
                if buttons[0]:
                    clickTime = moose_timer.getTime()
                
                # Rescaling (needed for Mac Retina screen)
                x = x * scaling_x
                y = y * scaling_y
                
                # Calculate distance from circle center
                dist = ((x - circle_center[0])**2 + (y - circle_center[1])**2)**0.5
            
                # Case 1: anticipating and cursor close to the nose
                if condition == 'anticipated' and dist <= distance_for_anticipated_below:
            
                    # Play the sound
                    bellowSound.play()
                    soundOnset = moose_timer.getTime()
                    
                    # While you wait, check for a button press
                    late_press = False
                    while moose_timer.getTime() - soundOnset < 1+jitter:
                        
                        if not late_press:
                            x_late, y_late = mouse.getPos()
                            buttons = mouse.getPressed()
                            if buttons[0]:
                                # print('Check this happens only once!')
                                clickTime = moose_timer.getTime()
                                x_late = x_late * scaling_x
                                y_late = y_late * scaling_y
                                late_press = True
                     
                    # Enter results: 
                    thisExp.addData('correct', 1)
                    if late_press:
                        thisExp.addData('click', 'late')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x_late)
                        thisExp.addData('click_y', y_late)
                    else:
                        thisExp.addData('click', 'no_late')
                        thisExp.addData('clickTime', None)
                        thisExp.addData('click_x', None)
                        thisExp.addData('click_y', None)
                    thisExp.addData('soundON', soundOnset)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    correct_trial_nb += 1        
                    
                    # End the trial
                    trial_ended = True
                    # correct_trial.finished = True
                    currentLoop.finished = True
                    continueRoutine = False
                    
                # Case 2: with a delay and clicking inside the nose    
                elif condition == 'delayed' and (buttons[0] and dist <= circle_radius):
            
                    # Schedule sound after delay and wait
                    core.wait(delay)
                    bellowSound.play()
                    soundOnset = moose_timer.getTime()
                    core.wait(1+jitter)
                    
                    # Enter results
                    thisExp.addData('correct', 1)
                    thisExp.addData('click', 'inside')
                    thisExp.addData('clickTime', clickTime)
                    thisExp.addData('click_x', x)
                    thisExp.addData('click_y', y)
                    thisExp.addData('soundON', soundOnset)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    correct_trial_nb += 1        
                    
                    # End the trial
                    trial_ended = True
                    # correct_trial.finished = True
                    currentLoop.finished = True
                    continueRoutine = False
            
                # Case 3: clicking but outside the correct window
                elif buttons[0]:
                    
                    # Display warning
                    warning_text.text = dt_txt['text_outside']
                    warning_text.draw()
                    moose.setAutoDraw(False)
                    win.flip()
                    core.wait(1)
                    
                    # Enter results
                    thisExp.addData('correct', 0)
                    thisExp.addData('click', 'outside')
                    thisExp.addData('clickTime', clickTime)
                    thisExp.addData('click_x', x)
                    thisExp.addData('click_y', y)
                    thisExp.addData('soundON', None)
                        
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    
                    # End the trial    
                    trial_ended = True
                    continueRoutine = False
            
                # Case 4: no click for 1s
                elif moose_timer.getTime() > 1.0:
                    
                    # Display warning
                    warning_text.text = dt_txt['text_no_click']
                    warning_text.draw()
                    moose.setAutoDraw(False)
                    win.flip()
                    core.wait(1)
                    
                    # Enter the results
                    thisExp.addData('correct', 0)
                    thisExp.addData('click', 'no_click')
                    thisExp.addData('clickTime', None)
                    thisExp.addData('click_x', None)
                    thisExp.addData('click_y', None)
                    thisExp.addData('soundON', None)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    
                    # End the trial    
                    trial_ended = True
                    continueRoutine = False                
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in MooseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Moose"-------
        for thisComponent in MooseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for correct_trial_training (TrialHandler)
        # get the image offset scheduled time and moose time
        if currentLoop.finished:
            thisExp.addData('scheduled_moose_time', soundOnset+1+jitter)
            thisExp.addData('moose_time', moose_timer.getTime())
        else:
            thisExp.addData('scheduled_moose_time', None)
            thisExp.addData('moose_time', None)
        
        
        # the Routine "Moose" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 99 repeats of 'correct_trial_training'
    
# completed 10 repeats of 'training_block'


# ------Prepare to start Routine "Pause1"-------
continueRoutine = True
# update component parameters for each repeat
# Hide cursor
win.mouseVisible = False

# Where we should be for each block (in min)
time_to_wait = [1, 3.1, 5.2, 9.1, 11.2, 15.1, 17.2] # 21.1
# time_to_wait = [0, 0, 0, 9, 11, 15, 17]

# Where we should be in sec
time_to_check = time_to_wait[block_nb]*60 + 10
# keep track of which components have finished
Pause1Components = [pause_text]
for thisComponent in Pause1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Pause1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Pause1"-------
while continueRoutine:
    # get current time
    t = Pause1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Pause1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *pause_text* updates
    if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        pause_text.frameNStart = frameN  # exact frame index
        pause_text.tStart = t  # local t and not account for scr refresh
        pause_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
        pause_text.setAutoDraw(True)
    # How are we doing timewise?
    win.flip()
    time_diff = time_to_check - tThisFlipGlobal
    
    if time_diff < 5:
        core.wait(5)
        continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Pause1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Pause1"-------
for thisComponent in Pause1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Pause1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Pause2"-------
continueRoutine = True
routineTimer.add(0.500000)
# update component parameters for each repeat
sound_1.setSound('A', secs=0.5, hamming=True)
sound_1.setVolume(1, log=False)
# keep track of which components have finished
Pause2Components = [sound_1]
for thisComponent in Pause2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Pause2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Pause2"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Pause2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Pause2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # start/stop sound_1
    if sound_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        sound_1.frameNStart = frameN  # exact frame index
        sound_1.tStart = t  # local t and not account for scr refresh
        sound_1.tStartRefresh = tThisFlipGlobal  # on global time
        sound_1.play(when=win)  # sync with win flip
    if sound_1.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > sound_1.tStartRefresh + 0.5-frameTolerance:
            # keep track of stop time/frame for later
            sound_1.tStop = t  # not accounting for scr refresh
            sound_1.frameNStop = frameN  # exact frame index
            win.timeOnFlip(sound_1, 'tStopRefresh')  # time at next scr refresh
            sound_1.stop()
    for countdown in [5, 4, 3, 2, 1]:
    
        warning_text.text = str(countdown)
        warning_text.draw()
        win.flip()
        core.wait(1)
    
    continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Pause2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Pause2"-------
for thisComponent in Pause2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
sound_1.stop()  # ensure sound has stopped at end of routine

# set up handler to look after randomisation of conditions etc
initial_adapt_block = data.TrialHandler(nReps=2, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='initial_adapt_block')
thisExp.addLoop(initial_adapt_block)  # add the loop to the experiment
thisInitial_adapt_block = initial_adapt_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisInitial_adapt_block.rgb)
if thisInitial_adapt_block != None:
    for paramName in thisInitial_adapt_block:
        exec('{} = thisInitial_adapt_block[paramName]'.format(paramName))

for thisInitial_adapt_block in initial_adapt_block:
    currentLoop = initial_adapt_block
    # abbreviate parameter names if possible (e.g. rgb = thisInitial_adapt_block.rgb)
    if thisInitial_adapt_block != None:
        for paramName in thisInitial_adapt_block:
            exec('{} = thisInitial_adapt_block[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Instruc_adapt"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # Define the block type, reinitialize counters, increment block number
    block_type = 'adapt'
    this_block_trial_nb = 0
    correct_trial_nb = 0
    block_nb +=1
    # keep track of which components have finished
    Instruc_adaptComponents = [Insctruction_adapt, key_resp_2]
    for thisComponent in Instruc_adaptComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Instruc_adaptClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Instruc_adapt"-------
    while continueRoutine:
        # get current time
        t = Instruc_adaptClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Instruc_adaptClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Insctruction_adapt* updates
        if Insctruction_adapt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Insctruction_adapt.frameNStart = frameN  # exact frame index
            Insctruction_adapt.tStart = t  # local t and not account for scr refresh
            Insctruction_adapt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Insctruction_adapt, 'tStartRefresh')  # time at next scr refresh
            Insctruction_adapt.setAutoDraw(True)
        
        # *key_resp_2* updates
        waitOnFlip = False
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instruc_adaptComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Instruc_adapt"-------
    for thisComponent in Instruc_adaptComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instruc_adapt" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    adapt_block1 = data.TrialHandler(nReps=42, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='adapt_block1')
    thisExp.addLoop(adapt_block1)  # add the loop to the experiment
    thisAdapt_block1 = adapt_block1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisAdapt_block1.rgb)
    if thisAdapt_block1 != None:
        for paramName in thisAdapt_block1:
            exec('{} = thisAdapt_block1[paramName]'.format(paramName))
    
    for thisAdapt_block1 in adapt_block1:
        currentLoop = adapt_block1
        # abbreviate parameter names if possible (e.g. rgb = thisAdapt_block1.rgb)
        if thisAdapt_block1 != None:
            for paramName in thisAdapt_block1:
                exec('{} = thisAdapt_block1[paramName]'.format(paramName))
        
        # set up handler to look after randomisation of conditions etc
        correct_trial_adapt1 = data.TrialHandler(nReps=99, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='correct_trial_adapt1')
        thisExp.addLoop(correct_trial_adapt1)  # add the loop to the experiment
        thisCorrect_trial_adapt1 = correct_trial_adapt1.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_adapt1.rgb)
        if thisCorrect_trial_adapt1 != None:
            for paramName in thisCorrect_trial_adapt1:
                exec('{} = thisCorrect_trial_adapt1[paramName]'.format(paramName))
        
        for thisCorrect_trial_adapt1 in correct_trial_adapt1:
            currentLoop = correct_trial_adapt1
            # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_adapt1.rgb)
            if thisCorrect_trial_adapt1 != None:
                for paramName in thisCorrect_trial_adapt1:
                    exec('{} = thisCorrect_trial_adapt1[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "Delay_for_adapt"-------
            continueRoutine = True
            # update component parameters for each repeat
            # keep track of which components have finished
            Delay_for_adaptComponents = []
            for thisComponent in Delay_for_adaptComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            Delay_for_adaptClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Delay_for_adapt"-------
            while continueRoutine:
                # get current time
                t = Delay_for_adaptClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Delay_for_adaptClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                sound_delay = 0.250
                continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Delay_for_adaptComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Delay_for_adapt"-------
            for thisComponent in Delay_for_adaptComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "Delay_for_adapt" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Fixation"-------
            continueRoutine = True
            # update component parameters for each repeat
            # Hide cursor
            win.mouseVisible = False
            
            # Fixation cross
            fix_size = 1.6   
            
            # Stimuli
            hor_line = visual.Line(win,  start=(-fix_size, 0), end=(fix_size, 0), lineWidth=5, units="cm")
            ver_line = visual.Line(win,  start=(0, -fix_size), end=(0, fix_size), lineWidth=5, units="cm")
            
            # Start timer
            fixation_timer = core.Clock()
            
            # Enter the counter for this trial
            thisExp.addData('block_nb', block_nb)
            thisExp.addData('total_trial_nb', total_trial_nb)
            thisExp.addData('this_block_trial_nb', this_block_trial_nb)
            thisExp.addData('correct_trial_nb', correct_trial_nb)
            
            # Enter the type of block
            thisExp.addData('block_type', block_type)
            
            # get the absolute time
            thisExp.addData('absolute_time', tThisFlipGlobal)
            
            # keep track of which components have finished
            FixationComponents = []
            for thisComponent in FixationComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            FixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Fixation"-------
            while continueRoutine:
                # get current time
                t = FixationClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=FixationClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                while fixation_timer.getTime() < 0.5:
                    hor_line.draw()
                    ver_line.draw()
                    win.flip()
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in FixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Fixation"-------
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Moose"-------
            continueRoutine = True
            # update component parameters for each repeat
            # setup some python lists for storing info about the mouse
            gotValidClick = False  # until a click is received
            # Set initial position (x, y) in cm
            mouse.setPos((-9.7, 0))
            
            # Show the cursor
            win.mouseVisible = True
            
            # Flags to track trial state
            trial_ended = False
            warning_shown = False
            
            # get the fixation time
            thisExp.addData('fixation_time', fixation_timer.getTime())
            
            # Start timer for 1-second limit
            moose_timer = core.Clock()
            
            # Schedule sound after delay
            # delay_choices = [0.2, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]  # seconds
            # sound_delay = random.choice(delay_choices)
            delay = float(sound_delay)
            if delay < 0:
                condition = 'anticipated'
            else:
                condition = 'delayed'
            
            # The jitter for the disappearance after the beginning of the trial
            jitter = random.randrange(-200, 200)/1000
            
            # Add some scheduled time
            thisExp.addData('scheduled_sound_delay', delay)
            thisExp.addData('scheduled_jitter', jitter)
            # keep track of which components have finished
            MooseComponents = [moose, mouse]
            for thisComponent in MooseComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            MooseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Moose"-------
            while continueRoutine:
                # get current time
                t = MooseClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=MooseClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *moose* updates
                if moose.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    moose.frameNStart = frameN  # exact frame index
                    moose.tStart = t  # local t and not account for scr refresh
                    moose.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(moose, 'tStartRefresh')  # time at next scr refresh
                    moose.setAutoDraw(True)
                if not trial_ended:
                
                    # Detecting cursor position and click
                    x, y = mouse.getPos()
                    buttons = mouse.getPressed()
                    if buttons[0]:
                        clickTime = moose_timer.getTime()
                    
                    # Rescaling (needed for Mac Retina screen)
                    x = x * scaling_x
                    y = y * scaling_y
                    
                    # Calculate distance from circle center
                    dist = ((x - circle_center[0])**2 + (y - circle_center[1])**2)**0.5
                
                    # Case 1: anticipating and cursor close to the nose
                    if condition == 'anticipated' and dist <= distance_for_anticipated_below:
                
                        # Play the sound
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        
                        # While you wait, check for a button press
                        late_press = False
                        while moose_timer.getTime() - soundOnset < 1+jitter:
                            
                            if not late_press:
                                x_late, y_late = mouse.getPos()
                                buttons = mouse.getPressed()
                                if buttons[0]:
                                    # print('Check this happens only once!')
                                    clickTime = moose_timer.getTime()
                                    x_late = x_late * scaling_x
                                    y_late = y_late * scaling_y
                                    late_press = True
                         
                        # Enter results: 
                        thisExp.addData('correct', 1)
                        if late_press:
                            thisExp.addData('click', 'late')
                            thisExp.addData('clickTime', clickTime)
                            thisExp.addData('click_x', x_late)
                            thisExp.addData('click_y', y_late)
                        else:
                            thisExp.addData('click', 'no_late')
                            thisExp.addData('clickTime', None)
                            thisExp.addData('click_x', None)
                            thisExp.addData('click_y', None)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                        
                    # Case 2: with a delay and clicking inside the nose    
                    elif condition == 'delayed' and (buttons[0] and dist <= circle_radius):
                
                        # Schedule sound after delay and wait
                        core.wait(delay)
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        core.wait(1+jitter)
                        
                        # Enter results
                        thisExp.addData('correct', 1)
                        thisExp.addData('click', 'inside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                
                    # Case 3: clicking but outside the correct window
                    elif buttons[0]:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_outside']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'outside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', None)
                            
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False
                
                    # Case 4: no click for 1s
                    elif moose_timer.getTime() > 1.0:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_no_click']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter the results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'no_click')
                        thisExp.addData('clickTime', None)
                        thisExp.addData('click_x', None)
                        thisExp.addData('click_y', None)
                        thisExp.addData('soundON', None)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False                
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in MooseComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Moose"-------
            for thisComponent in MooseComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for correct_trial_adapt1 (TrialHandler)
            # get the image offset scheduled time and moose time
            if currentLoop.finished:
                thisExp.addData('scheduled_moose_time', soundOnset+1+jitter)
                thisExp.addData('moose_time', moose_timer.getTime())
            else:
                thisExp.addData('scheduled_moose_time', None)
                thisExp.addData('moose_time', None)
            
            
            # the Routine "Moose" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 99 repeats of 'correct_trial_adapt1'
        
    # completed 42 repeats of 'adapt_block1'
    
    
    # ------Prepare to start Routine "Pause1"-------
    continueRoutine = True
    # update component parameters for each repeat
    # Hide cursor
    win.mouseVisible = False
    
    # Where we should be for each block (in min)
    time_to_wait = [1, 3.1, 5.2, 9.1, 11.2, 15.1, 17.2] # 21.1
    # time_to_wait = [0, 0, 0, 9, 11, 15, 17]
    
    # Where we should be in sec
    time_to_check = time_to_wait[block_nb]*60 + 10
    # keep track of which components have finished
    Pause1Components = [pause_text]
    for thisComponent in Pause1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause1"-------
    while continueRoutine:
        # get current time
        t = Pause1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_text* updates
        if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_text.frameNStart = frameN  # exact frame index
            pause_text.tStart = t  # local t and not account for scr refresh
            pause_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
            pause_text.setAutoDraw(True)
        # How are we doing timewise?
        win.flip()
        time_diff = time_to_check - tThisFlipGlobal
        
        if time_diff < 5:
            core.wait(5)
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause1"-------
    for thisComponent in Pause1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Pause1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Pause2"-------
    continueRoutine = True
    routineTimer.add(0.500000)
    # update component parameters for each repeat
    sound_1.setSound('A', secs=0.5, hamming=True)
    sound_1.setVolume(1, log=False)
    # keep track of which components have finished
    Pause2Components = [sound_1]
    for thisComponent in Pause2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Pause2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop sound_1
        if sound_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            sound_1.play(when=win)  # sync with win flip
        if sound_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sound_1.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                sound_1.tStop = t  # not accounting for scr refresh
                sound_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(sound_1, 'tStopRefresh')  # time at next scr refresh
                sound_1.stop()
        for countdown in [5, 4, 3, 2, 1]:
        
            warning_text.text = str(countdown)
            warning_text.draw()
            win.flip()
            core.wait(1)
        
        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause2"-------
    for thisComponent in Pause2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    sound_1.stop()  # ensure sound has stopped at end of routine
# completed 2 repeats of 'initial_adapt_block'


# set up handler to look after randomisation of conditions etc
test_and_adapt_block = data.TrialHandler(nReps=2, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='test_and_adapt_block')
thisExp.addLoop(test_and_adapt_block)  # add the loop to the experiment
thisTest_and_adapt_block = test_and_adapt_block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_and_adapt_block.rgb)
if thisTest_and_adapt_block != None:
    for paramName in thisTest_and_adapt_block:
        exec('{} = thisTest_and_adapt_block[paramName]'.format(paramName))

for thisTest_and_adapt_block in test_and_adapt_block:
    currentLoop = test_and_adapt_block
    # abbreviate parameter names if possible (e.g. rgb = thisTest_and_adapt_block.rgb)
    if thisTest_and_adapt_block != None:
        for paramName in thisTest_and_adapt_block:
            exec('{} = thisTest_and_adapt_block[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Instruc_test"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # Define the block type, reinitialize counters, increment block number
    block_type = 'test'
    this_block_trial_nb = 0
    correct_trial_nb = 0
    block_nb +=1
    # keep track of which components have finished
    Instruc_testComponents = [Instruction_test, key_resp_3]
    for thisComponent in Instruc_testComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Instruc_testClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Instruc_test"-------
    while continueRoutine:
        # get current time
        t = Instruc_testClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Instruc_testClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Instruction_test* updates
        if Instruction_test.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Instruction_test.frameNStart = frameN  # exact frame index
            Instruction_test.tStart = t  # local t and not account for scr refresh
            Instruction_test.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Instruction_test, 'tStartRefresh')  # time at next scr refresh
            Instruction_test.setAutoDraw(True)
        
        # *key_resp_3* updates
        waitOnFlip = False
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instruc_testComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Instruc_test"-------
    for thisComponent in Instruc_testComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instruc_test" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    test_block1 = data.TrialHandler(nReps=1, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('delay_test_block.csv'),
        seed=None, name='test_block1')
    thisExp.addLoop(test_block1)  # add the loop to the experiment
    thisTest_block1 = test_block1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTest_block1.rgb)
    if thisTest_block1 != None:
        for paramName in thisTest_block1:
            exec('{} = thisTest_block1[paramName]'.format(paramName))
    
    for thisTest_block1 in test_block1:
        currentLoop = test_block1
        # abbreviate parameter names if possible (e.g. rgb = thisTest_block1.rgb)
        if thisTest_block1 != None:
            for paramName in thisTest_block1:
                exec('{} = thisTest_block1[paramName]'.format(paramName))
        
        # set up handler to look after randomisation of conditions etc
        correct_trial_test1 = data.TrialHandler(nReps=99, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='correct_trial_test1')
        thisExp.addLoop(correct_trial_test1)  # add the loop to the experiment
        thisCorrect_trial_test1 = correct_trial_test1.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_test1.rgb)
        if thisCorrect_trial_test1 != None:
            for paramName in thisCorrect_trial_test1:
                exec('{} = thisCorrect_trial_test1[paramName]'.format(paramName))
        
        for thisCorrect_trial_test1 in correct_trial_test1:
            currentLoop = correct_trial_test1
            # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_test1.rgb)
            if thisCorrect_trial_test1 != None:
                for paramName in thisCorrect_trial_test1:
                    exec('{} = thisCorrect_trial_test1[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "Fixation"-------
            continueRoutine = True
            # update component parameters for each repeat
            # Hide cursor
            win.mouseVisible = False
            
            # Fixation cross
            fix_size = 1.6   
            
            # Stimuli
            hor_line = visual.Line(win,  start=(-fix_size, 0), end=(fix_size, 0), lineWidth=5, units="cm")
            ver_line = visual.Line(win,  start=(0, -fix_size), end=(0, fix_size), lineWidth=5, units="cm")
            
            # Start timer
            fixation_timer = core.Clock()
            
            # Enter the counter for this trial
            thisExp.addData('block_nb', block_nb)
            thisExp.addData('total_trial_nb', total_trial_nb)
            thisExp.addData('this_block_trial_nb', this_block_trial_nb)
            thisExp.addData('correct_trial_nb', correct_trial_nb)
            
            # Enter the type of block
            thisExp.addData('block_type', block_type)
            
            # get the absolute time
            thisExp.addData('absolute_time', tThisFlipGlobal)
            
            # keep track of which components have finished
            FixationComponents = []
            for thisComponent in FixationComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            FixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Fixation"-------
            while continueRoutine:
                # get current time
                t = FixationClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=FixationClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                while fixation_timer.getTime() < 0.5:
                    hor_line.draw()
                    ver_line.draw()
                    win.flip()
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in FixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Fixation"-------
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Moose"-------
            continueRoutine = True
            # update component parameters for each repeat
            # setup some python lists for storing info about the mouse
            gotValidClick = False  # until a click is received
            # Set initial position (x, y) in cm
            mouse.setPos((-9.7, 0))
            
            # Show the cursor
            win.mouseVisible = True
            
            # Flags to track trial state
            trial_ended = False
            warning_shown = False
            
            # get the fixation time
            thisExp.addData('fixation_time', fixation_timer.getTime())
            
            # Start timer for 1-second limit
            moose_timer = core.Clock()
            
            # Schedule sound after delay
            # delay_choices = [0.2, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]  # seconds
            # sound_delay = random.choice(delay_choices)
            delay = float(sound_delay)
            if delay < 0:
                condition = 'anticipated'
            else:
                condition = 'delayed'
            
            # The jitter for the disappearance after the beginning of the trial
            jitter = random.randrange(-200, 200)/1000
            
            # Add some scheduled time
            thisExp.addData('scheduled_sound_delay', delay)
            thisExp.addData('scheduled_jitter', jitter)
            # keep track of which components have finished
            MooseComponents = [moose, mouse]
            for thisComponent in MooseComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            MooseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Moose"-------
            while continueRoutine:
                # get current time
                t = MooseClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=MooseClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *moose* updates
                if moose.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    moose.frameNStart = frameN  # exact frame index
                    moose.tStart = t  # local t and not account for scr refresh
                    moose.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(moose, 'tStartRefresh')  # time at next scr refresh
                    moose.setAutoDraw(True)
                if not trial_ended:
                
                    # Detecting cursor position and click
                    x, y = mouse.getPos()
                    buttons = mouse.getPressed()
                    if buttons[0]:
                        clickTime = moose_timer.getTime()
                    
                    # Rescaling (needed for Mac Retina screen)
                    x = x * scaling_x
                    y = y * scaling_y
                    
                    # Calculate distance from circle center
                    dist = ((x - circle_center[0])**2 + (y - circle_center[1])**2)**0.5
                
                    # Case 1: anticipating and cursor close to the nose
                    if condition == 'anticipated' and dist <= distance_for_anticipated_below:
                
                        # Play the sound
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        
                        # While you wait, check for a button press
                        late_press = False
                        while moose_timer.getTime() - soundOnset < 1+jitter:
                            
                            if not late_press:
                                x_late, y_late = mouse.getPos()
                                buttons = mouse.getPressed()
                                if buttons[0]:
                                    # print('Check this happens only once!')
                                    clickTime = moose_timer.getTime()
                                    x_late = x_late * scaling_x
                                    y_late = y_late * scaling_y
                                    late_press = True
                         
                        # Enter results: 
                        thisExp.addData('correct', 1)
                        if late_press:
                            thisExp.addData('click', 'late')
                            thisExp.addData('clickTime', clickTime)
                            thisExp.addData('click_x', x_late)
                            thisExp.addData('click_y', y_late)
                        else:
                            thisExp.addData('click', 'no_late')
                            thisExp.addData('clickTime', None)
                            thisExp.addData('click_x', None)
                            thisExp.addData('click_y', None)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                        
                    # Case 2: with a delay and clicking inside the nose    
                    elif condition == 'delayed' and (buttons[0] and dist <= circle_radius):
                
                        # Schedule sound after delay and wait
                        core.wait(delay)
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        core.wait(1+jitter)
                        
                        # Enter results
                        thisExp.addData('correct', 1)
                        thisExp.addData('click', 'inside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                
                    # Case 3: clicking but outside the correct window
                    elif buttons[0]:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_outside']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'outside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', None)
                            
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False
                
                    # Case 4: no click for 1s
                    elif moose_timer.getTime() > 1.0:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_no_click']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter the results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'no_click')
                        thisExp.addData('clickTime', None)
                        thisExp.addData('click_x', None)
                        thisExp.addData('click_y', None)
                        thisExp.addData('soundON', None)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False                
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in MooseComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Moose"-------
            for thisComponent in MooseComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for correct_trial_test1 (TrialHandler)
            # get the image offset scheduled time and moose time
            if currentLoop.finished:
                thisExp.addData('scheduled_moose_time', soundOnset+1+jitter)
                thisExp.addData('moose_time', moose_timer.getTime())
            else:
                thisExp.addData('scheduled_moose_time', None)
                thisExp.addData('moose_time', None)
            
            
            # the Routine "Moose" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Scale"-------
            continueRoutine = True
            # update component parameters for each repeat
            # Set initial position (x, y) in cm
            mouse.setPos((0, -8))
            
            # Initialize the click
            isPressed = False
            
            # Start timer
            scale_timer = core.Clock()
            # setup some python lists for storing info about the mouse_scale
            gotValidClick = False  # until a click is received
            # keep track of which components have finished
            ScaleComponents = [mouse_scale]
            for thisComponent in ScaleComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ScaleClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Scale"-------
            while continueRoutine:
                # get current time
                t = ScaleClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ScaleClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                continueRoutine = True   # <-- Keep running unless told otherwise
                
                if currentLoop.finished:
                    
                    # Draw everything
                    scale_line.draw()
                    for t in ticks: t.draw()
                    general_label.draw()
                    left_label.draw()
                    center_label.draw()
                    right_label.draw()
                    red_x.draw()
                    
                    if not isPressed:
                        x, y = mouse_scale.getPos()
                        buttons_scale = mouse_scale.getPressed()
                        x = x * scaling_x
                        y = y * scaling_y
                    
                    # Check for clicks
                    if buttons_scale[0] and red_x.opacity == 0.0:  # only accept first click
                        if x_min <= x <= x_max and abs(y-y_pos) < 0.5:  # clicked near line
                            isPressed = True
                            red_x.pos = (x, y_pos)
                            red_x.opacity = 1.0
                            rating_time = scale_timer.getTime()
                            # response_time = tThisFlipGlobal
                            
                    # Hide X and end after 0.5s
                    if red_x.opacity == 1.0 and (scale_timer.getTime() - rating_time) > 0.5:
                        
                        # In preparation of the next trial
                        red_x.opacity = 0.0
                        
                        # Save response (in %)
                        rating = (x - x_min) / (x_max - x_min) * 100
                        thisExp.addData("rating", rating)
                        thisExp.addData("rating_time", rating_time)
                        
                        # End
                        isPressed = False
                        continueRoutine = False
                        
                else:
                    
                    thisExp.addData("rating", None)
                    thisExp.addData("rating_time", None)
                    continueRoutine = False
                
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ScaleComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Scale"-------
            for thisComponent in ScaleComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for correct_trial_test1 (TrialHandler)
            # the Routine "Scale" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 99 repeats of 'correct_trial_test1'
        
    # completed 1 repeats of 'test_block1'
    
    
    # ------Prepare to start Routine "Pause1"-------
    continueRoutine = True
    # update component parameters for each repeat
    # Hide cursor
    win.mouseVisible = False
    
    # Where we should be for each block (in min)
    time_to_wait = [1, 3.1, 5.2, 9.1, 11.2, 15.1, 17.2] # 21.1
    # time_to_wait = [0, 0, 0, 9, 11, 15, 17]
    
    # Where we should be in sec
    time_to_check = time_to_wait[block_nb]*60 + 10
    # keep track of which components have finished
    Pause1Components = [pause_text]
    for thisComponent in Pause1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause1"-------
    while continueRoutine:
        # get current time
        t = Pause1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_text* updates
        if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_text.frameNStart = frameN  # exact frame index
            pause_text.tStart = t  # local t and not account for scr refresh
            pause_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
            pause_text.setAutoDraw(True)
        # How are we doing timewise?
        win.flip()
        time_diff = time_to_check - tThisFlipGlobal
        
        if time_diff < 5:
            core.wait(5)
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause1"-------
    for thisComponent in Pause1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Pause1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Pause2"-------
    continueRoutine = True
    routineTimer.add(0.500000)
    # update component parameters for each repeat
    sound_1.setSound('A', secs=0.5, hamming=True)
    sound_1.setVolume(1, log=False)
    # keep track of which components have finished
    Pause2Components = [sound_1]
    for thisComponent in Pause2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Pause2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop sound_1
        if sound_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            sound_1.play(when=win)  # sync with win flip
        if sound_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sound_1.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                sound_1.tStop = t  # not accounting for scr refresh
                sound_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(sound_1, 'tStopRefresh')  # time at next scr refresh
                sound_1.stop()
        for countdown in [5, 4, 3, 2, 1]:
        
            warning_text.text = str(countdown)
            warning_text.draw()
            win.flip()
            core.wait(1)
        
        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause2"-------
    for thisComponent in Pause2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    sound_1.stop()  # ensure sound has stopped at end of routine
    
    # ------Prepare to start Routine "Instruc_adapt"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # Define the block type, reinitialize counters, increment block number
    block_type = 'adapt'
    this_block_trial_nb = 0
    correct_trial_nb = 0
    block_nb +=1
    # keep track of which components have finished
    Instruc_adaptComponents = [Insctruction_adapt, key_resp_2]
    for thisComponent in Instruc_adaptComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Instruc_adaptClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Instruc_adapt"-------
    while continueRoutine:
        # get current time
        t = Instruc_adaptClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Instruc_adaptClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Insctruction_adapt* updates
        if Insctruction_adapt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Insctruction_adapt.frameNStart = frameN  # exact frame index
            Insctruction_adapt.tStart = t  # local t and not account for scr refresh
            Insctruction_adapt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Insctruction_adapt, 'tStartRefresh')  # time at next scr refresh
            Insctruction_adapt.setAutoDraw(True)
        
        # *key_resp_2* updates
        waitOnFlip = False
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Instruc_adaptComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Instruc_adapt"-------
    for thisComponent in Instruc_adaptComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Instruc_adapt" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    adapt_block2 = data.TrialHandler(nReps=42, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='adapt_block2')
    thisExp.addLoop(adapt_block2)  # add the loop to the experiment
    thisAdapt_block2 = adapt_block2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisAdapt_block2.rgb)
    if thisAdapt_block2 != None:
        for paramName in thisAdapt_block2:
            exec('{} = thisAdapt_block2[paramName]'.format(paramName))
    
    for thisAdapt_block2 in adapt_block2:
        currentLoop = adapt_block2
        # abbreviate parameter names if possible (e.g. rgb = thisAdapt_block2.rgb)
        if thisAdapt_block2 != None:
            for paramName in thisAdapt_block2:
                exec('{} = thisAdapt_block2[paramName]'.format(paramName))
        
        # set up handler to look after randomisation of conditions etc
        correct_trial_adapt2 = data.TrialHandler(nReps=99, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='correct_trial_adapt2')
        thisExp.addLoop(correct_trial_adapt2)  # add the loop to the experiment
        thisCorrect_trial_adapt2 = correct_trial_adapt2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_adapt2.rgb)
        if thisCorrect_trial_adapt2 != None:
            for paramName in thisCorrect_trial_adapt2:
                exec('{} = thisCorrect_trial_adapt2[paramName]'.format(paramName))
        
        for thisCorrect_trial_adapt2 in correct_trial_adapt2:
            currentLoop = correct_trial_adapt2
            # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_adapt2.rgb)
            if thisCorrect_trial_adapt2 != None:
                for paramName in thisCorrect_trial_adapt2:
                    exec('{} = thisCorrect_trial_adapt2[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "Delay_for_adapt"-------
            continueRoutine = True
            # update component parameters for each repeat
            # keep track of which components have finished
            Delay_for_adaptComponents = []
            for thisComponent in Delay_for_adaptComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            Delay_for_adaptClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Delay_for_adapt"-------
            while continueRoutine:
                # get current time
                t = Delay_for_adaptClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=Delay_for_adaptClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                sound_delay = 0.250
                continueRoutine = False
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Delay_for_adaptComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Delay_for_adapt"-------
            for thisComponent in Delay_for_adaptComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "Delay_for_adapt" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Fixation"-------
            continueRoutine = True
            # update component parameters for each repeat
            # Hide cursor
            win.mouseVisible = False
            
            # Fixation cross
            fix_size = 1.6   
            
            # Stimuli
            hor_line = visual.Line(win,  start=(-fix_size, 0), end=(fix_size, 0), lineWidth=5, units="cm")
            ver_line = visual.Line(win,  start=(0, -fix_size), end=(0, fix_size), lineWidth=5, units="cm")
            
            # Start timer
            fixation_timer = core.Clock()
            
            # Enter the counter for this trial
            thisExp.addData('block_nb', block_nb)
            thisExp.addData('total_trial_nb', total_trial_nb)
            thisExp.addData('this_block_trial_nb', this_block_trial_nb)
            thisExp.addData('correct_trial_nb', correct_trial_nb)
            
            # Enter the type of block
            thisExp.addData('block_type', block_type)
            
            # get the absolute time
            thisExp.addData('absolute_time', tThisFlipGlobal)
            
            # keep track of which components have finished
            FixationComponents = []
            for thisComponent in FixationComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            FixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Fixation"-------
            while continueRoutine:
                # get current time
                t = FixationClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=FixationClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                while fixation_timer.getTime() < 0.5:
                    hor_line.draw()
                    ver_line.draw()
                    win.flip()
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in FixationComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Fixation"-------
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # ------Prepare to start Routine "Moose"-------
            continueRoutine = True
            # update component parameters for each repeat
            # setup some python lists for storing info about the mouse
            gotValidClick = False  # until a click is received
            # Set initial position (x, y) in cm
            mouse.setPos((-9.7, 0))
            
            # Show the cursor
            win.mouseVisible = True
            
            # Flags to track trial state
            trial_ended = False
            warning_shown = False
            
            # get the fixation time
            thisExp.addData('fixation_time', fixation_timer.getTime())
            
            # Start timer for 1-second limit
            moose_timer = core.Clock()
            
            # Schedule sound after delay
            # delay_choices = [0.2, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]  # seconds
            # sound_delay = random.choice(delay_choices)
            delay = float(sound_delay)
            if delay < 0:
                condition = 'anticipated'
            else:
                condition = 'delayed'
            
            # The jitter for the disappearance after the beginning of the trial
            jitter = random.randrange(-200, 200)/1000
            
            # Add some scheduled time
            thisExp.addData('scheduled_sound_delay', delay)
            thisExp.addData('scheduled_jitter', jitter)
            # keep track of which components have finished
            MooseComponents = [moose, mouse]
            for thisComponent in MooseComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            MooseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            
            # -------Run Routine "Moose"-------
            while continueRoutine:
                # get current time
                t = MooseClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=MooseClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *moose* updates
                if moose.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    moose.frameNStart = frameN  # exact frame index
                    moose.tStart = t  # local t and not account for scr refresh
                    moose.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(moose, 'tStartRefresh')  # time at next scr refresh
                    moose.setAutoDraw(True)
                if not trial_ended:
                
                    # Detecting cursor position and click
                    x, y = mouse.getPos()
                    buttons = mouse.getPressed()
                    if buttons[0]:
                        clickTime = moose_timer.getTime()
                    
                    # Rescaling (needed for Mac Retina screen)
                    x = x * scaling_x
                    y = y * scaling_y
                    
                    # Calculate distance from circle center
                    dist = ((x - circle_center[0])**2 + (y - circle_center[1])**2)**0.5
                
                    # Case 1: anticipating and cursor close to the nose
                    if condition == 'anticipated' and dist <= distance_for_anticipated_below:
                
                        # Play the sound
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        
                        # While you wait, check for a button press
                        late_press = False
                        while moose_timer.getTime() - soundOnset < 1+jitter:
                            
                            if not late_press:
                                x_late, y_late = mouse.getPos()
                                buttons = mouse.getPressed()
                                if buttons[0]:
                                    # print('Check this happens only once!')
                                    clickTime = moose_timer.getTime()
                                    x_late = x_late * scaling_x
                                    y_late = y_late * scaling_y
                                    late_press = True
                         
                        # Enter results: 
                        thisExp.addData('correct', 1)
                        if late_press:
                            thisExp.addData('click', 'late')
                            thisExp.addData('clickTime', clickTime)
                            thisExp.addData('click_x', x_late)
                            thisExp.addData('click_y', y_late)
                        else:
                            thisExp.addData('click', 'no_late')
                            thisExp.addData('clickTime', None)
                            thisExp.addData('click_x', None)
                            thisExp.addData('click_y', None)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                        
                    # Case 2: with a delay and clicking inside the nose    
                    elif condition == 'delayed' and (buttons[0] and dist <= circle_radius):
                
                        # Schedule sound after delay and wait
                        core.wait(delay)
                        bellowSound.play()
                        soundOnset = moose_timer.getTime()
                        core.wait(1+jitter)
                        
                        # Enter results
                        thisExp.addData('correct', 1)
                        thisExp.addData('click', 'inside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', soundOnset)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        correct_trial_nb += 1        
                        
                        # End the trial
                        trial_ended = True
                        # correct_trial.finished = True
                        currentLoop.finished = True
                        continueRoutine = False
                
                    # Case 3: clicking but outside the correct window
                    elif buttons[0]:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_outside']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'outside')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x)
                        thisExp.addData('click_y', y)
                        thisExp.addData('soundON', None)
                            
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False
                
                    # Case 4: no click for 1s
                    elif moose_timer.getTime() > 1.0:
                        
                        # Display warning
                        warning_text.text = dt_txt['text_no_click']
                        warning_text.draw()
                        moose.setAutoDraw(False)
                        win.flip()
                        core.wait(1)
                        
                        # Enter the results
                        thisExp.addData('correct', 0)
                        thisExp.addData('click', 'no_click')
                        thisExp.addData('clickTime', None)
                        thisExp.addData('click_x', None)
                        thisExp.addData('click_y', None)
                        thisExp.addData('soundON', None)
                        
                        # Increment counters
                        total_trial_nb += 1
                        this_block_trial_nb += 1
                        
                        # End the trial    
                        trial_ended = True
                        continueRoutine = False                
                
                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in MooseComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "Moose"-------
            for thisComponent in MooseComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for correct_trial_adapt2 (TrialHandler)
            # get the image offset scheduled time and moose time
            if currentLoop.finished:
                thisExp.addData('scheduled_moose_time', soundOnset+1+jitter)
                thisExp.addData('moose_time', moose_timer.getTime())
            else:
                thisExp.addData('scheduled_moose_time', None)
                thisExp.addData('moose_time', None)
            
            
            # the Routine "Moose" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 99 repeats of 'correct_trial_adapt2'
        
    # completed 42 repeats of 'adapt_block2'
    
    
    # ------Prepare to start Routine "Pause1"-------
    continueRoutine = True
    # update component parameters for each repeat
    # Hide cursor
    win.mouseVisible = False
    
    # Where we should be for each block (in min)
    time_to_wait = [1, 3.1, 5.2, 9.1, 11.2, 15.1, 17.2] # 21.1
    # time_to_wait = [0, 0, 0, 9, 11, 15, 17]
    
    # Where we should be in sec
    time_to_check = time_to_wait[block_nb]*60 + 10
    # keep track of which components have finished
    Pause1Components = [pause_text]
    for thisComponent in Pause1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause1"-------
    while continueRoutine:
        # get current time
        t = Pause1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *pause_text* updates
        if pause_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            pause_text.frameNStart = frameN  # exact frame index
            pause_text.tStart = t  # local t and not account for scr refresh
            pause_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(pause_text, 'tStartRefresh')  # time at next scr refresh
            pause_text.setAutoDraw(True)
        # How are we doing timewise?
        win.flip()
        time_diff = time_to_check - tThisFlipGlobal
        
        if time_diff < 5:
            core.wait(5)
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause1"-------
    for thisComponent in Pause1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Pause1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Pause2"-------
    continueRoutine = True
    routineTimer.add(0.500000)
    # update component parameters for each repeat
    sound_1.setSound('A', secs=0.5, hamming=True)
    sound_1.setVolume(1, log=False)
    # keep track of which components have finished
    Pause2Components = [sound_1]
    for thisComponent in Pause2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Pause2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Pause2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Pause2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Pause2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop sound_1
        if sound_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            sound_1.play(when=win)  # sync with win flip
        if sound_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > sound_1.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                sound_1.tStop = t  # not accounting for scr refresh
                sound_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(sound_1, 'tStopRefresh')  # time at next scr refresh
                sound_1.stop()
        for countdown in [5, 4, 3, 2, 1]:
        
            warning_text.text = str(countdown)
            warning_text.draw()
            win.flip()
            core.wait(1)
        
        continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Pause2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Pause2"-------
    for thisComponent in Pause2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    sound_1.stop()  # ensure sound has stopped at end of routine
# completed 2 repeats of 'test_and_adapt_block'


# ------Prepare to start Routine "Instruc_test"-------
continueRoutine = True
# update component parameters for each repeat
key_resp_3.keys = []
key_resp_3.rt = []
_key_resp_3_allKeys = []
# Define the block type, reinitialize counters, increment block number
block_type = 'test'
this_block_trial_nb = 0
correct_trial_nb = 0
block_nb +=1
# keep track of which components have finished
Instruc_testComponents = [Instruction_test, key_resp_3]
for thisComponent in Instruc_testComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Instruc_testClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instruc_test"-------
while continueRoutine:
    # get current time
    t = Instruc_testClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Instruc_testClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Instruction_test* updates
    if Instruction_test.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Instruction_test.frameNStart = frameN  # exact frame index
        Instruction_test.tStart = t  # local t and not account for scr refresh
        Instruction_test.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Instruction_test, 'tStartRefresh')  # time at next scr refresh
        Instruction_test.setAutoDraw(True)
    
    # *key_resp_3* updates
    waitOnFlip = False
    if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.tStart = t  # local t and not account for scr refresh
        key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_3.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_3.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_3_allKeys.extend(theseKeys)
        if len(_key_resp_3_allKeys):
            key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
            key_resp_3.rt = _key_resp_3_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instruc_testComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instruc_test"-------
for thisComponent in Instruc_testComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instruc_test" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
test_block2 = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('delay_test_block.csv'),
    seed=None, name='test_block2')
thisExp.addLoop(test_block2)  # add the loop to the experiment
thisTest_block2 = test_block2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTest_block2.rgb)
if thisTest_block2 != None:
    for paramName in thisTest_block2:
        exec('{} = thisTest_block2[paramName]'.format(paramName))

for thisTest_block2 in test_block2:
    currentLoop = test_block2
    # abbreviate parameter names if possible (e.g. rgb = thisTest_block2.rgb)
    if thisTest_block2 != None:
        for paramName in thisTest_block2:
            exec('{} = thisTest_block2[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    correct_trial_test2 = data.TrialHandler(nReps=99, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='correct_trial_test2')
    thisExp.addLoop(correct_trial_test2)  # add the loop to the experiment
    thisCorrect_trial_test2 = correct_trial_test2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_test2.rgb)
    if thisCorrect_trial_test2 != None:
        for paramName in thisCorrect_trial_test2:
            exec('{} = thisCorrect_trial_test2[paramName]'.format(paramName))
    
    for thisCorrect_trial_test2 in correct_trial_test2:
        currentLoop = correct_trial_test2
        # abbreviate parameter names if possible (e.g. rgb = thisCorrect_trial_test2.rgb)
        if thisCorrect_trial_test2 != None:
            for paramName in thisCorrect_trial_test2:
                exec('{} = thisCorrect_trial_test2[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Fixation"-------
        continueRoutine = True
        # update component parameters for each repeat
        # Hide cursor
        win.mouseVisible = False
        
        # Fixation cross
        fix_size = 1.6   
        
        # Stimuli
        hor_line = visual.Line(win,  start=(-fix_size, 0), end=(fix_size, 0), lineWidth=5, units="cm")
        ver_line = visual.Line(win,  start=(0, -fix_size), end=(0, fix_size), lineWidth=5, units="cm")
        
        # Start timer
        fixation_timer = core.Clock()
        
        # Enter the counter for this trial
        thisExp.addData('block_nb', block_nb)
        thisExp.addData('total_trial_nb', total_trial_nb)
        thisExp.addData('this_block_trial_nb', this_block_trial_nb)
        thisExp.addData('correct_trial_nb', correct_trial_nb)
        
        # Enter the type of block
        thisExp.addData('block_type', block_type)
        
        # get the absolute time
        thisExp.addData('absolute_time', tThisFlipGlobal)
        
        # keep track of which components have finished
        FixationComponents = []
        for thisComponent in FixationComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        FixationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Fixation"-------
        while continueRoutine:
            # get current time
            t = FixationClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=FixationClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            while fixation_timer.getTime() < 0.5:
                hor_line.draw()
                ver_line.draw()
                win.flip()
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FixationComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Fixation"-------
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Moose"-------
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the mouse
        gotValidClick = False  # until a click is received
        # Set initial position (x, y) in cm
        mouse.setPos((-9.7, 0))
        
        # Show the cursor
        win.mouseVisible = True
        
        # Flags to track trial state
        trial_ended = False
        warning_shown = False
        
        # get the fixation time
        thisExp.addData('fixation_time', fixation_timer.getTime())
        
        # Start timer for 1-second limit
        moose_timer = core.Clock()
        
        # Schedule sound after delay
        # delay_choices = [0.2, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]  # seconds
        # sound_delay = random.choice(delay_choices)
        delay = float(sound_delay)
        if delay < 0:
            condition = 'anticipated'
        else:
            condition = 'delayed'
        
        # The jitter for the disappearance after the beginning of the trial
        jitter = random.randrange(-200, 200)/1000
        
        # Add some scheduled time
        thisExp.addData('scheduled_sound_delay', delay)
        thisExp.addData('scheduled_jitter', jitter)
        # keep track of which components have finished
        MooseComponents = [moose, mouse]
        for thisComponent in MooseComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        MooseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Moose"-------
        while continueRoutine:
            # get current time
            t = MooseClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=MooseClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *moose* updates
            if moose.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                moose.frameNStart = frameN  # exact frame index
                moose.tStart = t  # local t and not account for scr refresh
                moose.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moose, 'tStartRefresh')  # time at next scr refresh
                moose.setAutoDraw(True)
            if not trial_ended:
            
                # Detecting cursor position and click
                x, y = mouse.getPos()
                buttons = mouse.getPressed()
                if buttons[0]:
                    clickTime = moose_timer.getTime()
                
                # Rescaling (needed for Mac Retina screen)
                x = x * scaling_x
                y = y * scaling_y
                
                # Calculate distance from circle center
                dist = ((x - circle_center[0])**2 + (y - circle_center[1])**2)**0.5
            
                # Case 1: anticipating and cursor close to the nose
                if condition == 'anticipated' and dist <= distance_for_anticipated_below:
            
                    # Play the sound
                    bellowSound.play()
                    soundOnset = moose_timer.getTime()
                    
                    # While you wait, check for a button press
                    late_press = False
                    while moose_timer.getTime() - soundOnset < 1+jitter:
                        
                        if not late_press:
                            x_late, y_late = mouse.getPos()
                            buttons = mouse.getPressed()
                            if buttons[0]:
                                # print('Check this happens only once!')
                                clickTime = moose_timer.getTime()
                                x_late = x_late * scaling_x
                                y_late = y_late * scaling_y
                                late_press = True
                     
                    # Enter results: 
                    thisExp.addData('correct', 1)
                    if late_press:
                        thisExp.addData('click', 'late')
                        thisExp.addData('clickTime', clickTime)
                        thisExp.addData('click_x', x_late)
                        thisExp.addData('click_y', y_late)
                    else:
                        thisExp.addData('click', 'no_late')
                        thisExp.addData('clickTime', None)
                        thisExp.addData('click_x', None)
                        thisExp.addData('click_y', None)
                    thisExp.addData('soundON', soundOnset)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    correct_trial_nb += 1        
                    
                    # End the trial
                    trial_ended = True
                    # correct_trial.finished = True
                    currentLoop.finished = True
                    continueRoutine = False
                    
                # Case 2: with a delay and clicking inside the nose    
                elif condition == 'delayed' and (buttons[0] and dist <= circle_radius):
            
                    # Schedule sound after delay and wait
                    core.wait(delay)
                    bellowSound.play()
                    soundOnset = moose_timer.getTime()
                    core.wait(1+jitter)
                    
                    # Enter results
                    thisExp.addData('correct', 1)
                    thisExp.addData('click', 'inside')
                    thisExp.addData('clickTime', clickTime)
                    thisExp.addData('click_x', x)
                    thisExp.addData('click_y', y)
                    thisExp.addData('soundON', soundOnset)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    correct_trial_nb += 1        
                    
                    # End the trial
                    trial_ended = True
                    # correct_trial.finished = True
                    currentLoop.finished = True
                    continueRoutine = False
            
                # Case 3: clicking but outside the correct window
                elif buttons[0]:
                    
                    # Display warning
                    warning_text.text = dt_txt['text_outside']
                    warning_text.draw()
                    moose.setAutoDraw(False)
                    win.flip()
                    core.wait(1)
                    
                    # Enter results
                    thisExp.addData('correct', 0)
                    thisExp.addData('click', 'outside')
                    thisExp.addData('clickTime', clickTime)
                    thisExp.addData('click_x', x)
                    thisExp.addData('click_y', y)
                    thisExp.addData('soundON', None)
                        
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    
                    # End the trial    
                    trial_ended = True
                    continueRoutine = False
            
                # Case 4: no click for 1s
                elif moose_timer.getTime() > 1.0:
                    
                    # Display warning
                    warning_text.text = dt_txt['text_no_click']
                    warning_text.draw()
                    moose.setAutoDraw(False)
                    win.flip()
                    core.wait(1)
                    
                    # Enter the results
                    thisExp.addData('correct', 0)
                    thisExp.addData('click', 'no_click')
                    thisExp.addData('clickTime', None)
                    thisExp.addData('click_x', None)
                    thisExp.addData('click_y', None)
                    thisExp.addData('soundON', None)
                    
                    # Increment counters
                    total_trial_nb += 1
                    this_block_trial_nb += 1
                    
                    # End the trial    
                    trial_ended = True
                    continueRoutine = False                
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in MooseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Moose"-------
        for thisComponent in MooseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for correct_trial_test2 (TrialHandler)
        # get the image offset scheduled time and moose time
        if currentLoop.finished:
            thisExp.addData('scheduled_moose_time', soundOnset+1+jitter)
            thisExp.addData('moose_time', moose_timer.getTime())
        else:
            thisExp.addData('scheduled_moose_time', None)
            thisExp.addData('moose_time', None)
        
        
        # the Routine "Moose" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # ------Prepare to start Routine "Scale"-------
        continueRoutine = True
        # update component parameters for each repeat
        # Set initial position (x, y) in cm
        mouse.setPos((0, -8))
        
        # Initialize the click
        isPressed = False
        
        # Start timer
        scale_timer = core.Clock()
        # setup some python lists for storing info about the mouse_scale
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        ScaleComponents = [mouse_scale]
        for thisComponent in ScaleComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        ScaleClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Scale"-------
        while continueRoutine:
            # get current time
            t = ScaleClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=ScaleClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            continueRoutine = True   # <-- Keep running unless told otherwise
            
            if currentLoop.finished:
                
                # Draw everything
                scale_line.draw()
                for t in ticks: t.draw()
                general_label.draw()
                left_label.draw()
                center_label.draw()
                right_label.draw()
                red_x.draw()
                
                if not isPressed:
                    x, y = mouse_scale.getPos()
                    buttons_scale = mouse_scale.getPressed()
                    x = x * scaling_x
                    y = y * scaling_y
                
                # Check for clicks
                if buttons_scale[0] and red_x.opacity == 0.0:  # only accept first click
                    if x_min <= x <= x_max and abs(y-y_pos) < 0.5:  # clicked near line
                        isPressed = True
                        red_x.pos = (x, y_pos)
                        red_x.opacity = 1.0
                        rating_time = scale_timer.getTime()
                        # response_time = tThisFlipGlobal
                        
                # Hide X and end after 0.5s
                if red_x.opacity == 1.0 and (scale_timer.getTime() - rating_time) > 0.5:
                    
                    # In preparation of the next trial
                    red_x.opacity = 0.0
                    
                    # Save response (in %)
                    rating = (x - x_min) / (x_max - x_min) * 100
                    thisExp.addData("rating", rating)
                    thisExp.addData("rating_time", rating_time)
                    
                    # End
                    isPressed = False
                    continueRoutine = False
                    
            else:
                
                thisExp.addData("rating", None)
                thisExp.addData("rating_time", None)
                continueRoutine = False
            
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ScaleComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Scale"-------
        for thisComponent in ScaleComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for correct_trial_test2 (TrialHandler)
        # the Routine "Scale" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 99 repeats of 'correct_trial_test2'
    
# completed 1 repeats of 'test_block2'


# ------Prepare to start Routine "Finalize"-------
continueRoutine = True
# update component parameters for each repeat
import pandas as pd

# First, ask ExperimentHandler to save as wide text
thisExp.saveAsWideText(thisExp.dataFileName + '_raw.csv')

# load, drop unwanted columns, and save a clean copy
df = pd.read_csv(thisExp.dataFileName + '_raw.csv')
df = df.drop(columns=[c for c in df.columns if '.this' in c], errors='ignore')
df = df.drop(columns=['sound_delay'], errors='ignore')
df.to_csv(thisExp.dataFileName + '_clean.csv', index=False)

key_resp_4.keys = []
key_resp_4.rt = []
_key_resp_4_allKeys = []
# keep track of which components have finished
FinalizeComponents = [GoodBye, key_resp_4]
for thisComponent in FinalizeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
FinalizeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Finalize"-------
while continueRoutine:
    # get current time
    t = FinalizeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=FinalizeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *GoodBye* updates
    if GoodBye.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        GoodBye.frameNStart = frameN  # exact frame index
        GoodBye.tStart = t  # local t and not account for scr refresh
        GoodBye.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(GoodBye, 'tStartRefresh')  # time at next scr refresh
        GoodBye.setAutoDraw(True)
    
    # *key_resp_4* updates
    waitOnFlip = False
    if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.tStart = t  # local t and not account for scr refresh
        key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp_4.status == STARTED and not waitOnFlip:
        theseKeys = key_resp_4.getKeys(keyList=['a'], waitRelease=False)
        _key_resp_4_allKeys.extend(theseKeys)
        if len(_key_resp_4_allKeys):
            key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
            key_resp_4.rt = _key_resp_4_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in FinalizeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Finalize"-------
for thisComponent in FinalizeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('GoodBye.started', GoodBye.tStartRefresh)
thisExp.addData('GoodBye.stopped', GoodBye.tStopRefresh)
# the Routine "Finalize" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
