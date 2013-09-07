import time
import maestro
import sonic
import random
import scrnio

#--------------------------
# CONSTANTS AND VARIABLES
#--------------------------

# Servo channel assignment constants
servoSteer=0     #steering
servoDrive=1     #motor drive
servoScanner=5   #sonar scanner

# Drive and Steering movement parameter pair constants
moveStop    = (6000,6025)   #Stop forward motion and Steer straight
moveFront   = (6500,6025)   #Move forward and Steer straight
moveLeft    = (6000,5525)   #Stop forward motion and Steer left
moveRight   = (6000,6525)   #Stop forward motion and Steer right

# Define autonomous movement variables
autoMode = ""        #Autonomus mode is either "SCAN" or "MOVE".
autoTimer = 0        #Timer in seconds for how long current autoMode is to run.
autoDirection = ""   #Direction automous mode is either Scanning and/or Moving - "FORWARD", "LEFT", "RIGHT"

# Sonar safe distance constants and variable
safeDistance = 40    #Minimum safe distance in centimeters
safeTime = 1.5         #Number of seconds required, without object detection, to be consider safe to move.
safeTimer = safeTime #Timer will start at SafeTime and counts down to 0, if no obstacles seen.

# Main Loop delay. Keep delay 0.1secs or higher, so as to not overwhelm sonar. 
looptime = 0.2       #Seconds of delay between main loop cycles

# Messaging text
global msgText

#------------
# FUNCTIONS
#------------

# Display a status message
# 
def message(text):
    global msgText
    msgText = text
    
    
# Randomly returns a direction LEFT, RIGHT, or FRONT
# FRONT is twice as likely as LEFT or RIGHT
def rndDirection():
    Dirs = {1:"LEFT",2:"RIGHT",3:"FRONT",4:"FRONT"}
    r = random.randrange(1,4)
    return Dirs[r]

# Set scanner to scan in the direction indicated.  This uses Maestro scripts 
# to perform the osciliation of the servo.  Directions are "LEFT", "RIGHT", and "FRONT.
# A special case, "CENTER", points sensor straight-ahead and halts oscilations.  
def setScanner(direction):
    # Script subroutines are numbered on the Maestro
    Subs = {"CENTER":0,"FRONT":1,"LEFT":2,"RIGHT":3}
    servo.runScriptSub(Subs[direction])

#
# Randomly select a direcion to scan which will be where we move next, if safe.
# Returns: autoMode='SCAN', autoTimer=5, autoDirection={random direction} 
#
def startScanning(currDirection):
    autoMode = "SCAN"
    autoTimer = 5   #Set time so that Scan will wait no more than 5secs before scanning in another direction
    autoDirection = rndDirection()
    # If this is a different direction than current, set the scanner to the new direction
    if autoDirection != currDirection:
        setScanner(autoDirection)
    message("Scanning "+autoDirection+" for "+str(autoTimer)+"s.")
    return (autoMode,autoTimer,autoDirection)    

#
# Set drive servos to target positions measured in 1/4 micro-second pulse widths.
# Pass 'targets' paramaeter in the format (drivetarget,steertarget).
# Use the constants 'moveStop', 'moveFront', and so on as the parameter.
#
def setDrive(targets):
    global servoDrive, servoSteer
    servo.setTarget(servoDrive,targets[0])
    servo.setTarget(servoSteer,targets[1])

#
# Once it has been determined it is safe to move, calling this subroutine
# will set the automous mode to MOVE, pick a random direction to move, determine
# a random time to move in that direction, and issue set the servos in motion.
#
def startMoving(autoDirection):
    global moveFront,moveLeft,moveRight
    autoMode = "MOVE"
    if autoDirection == "FRONT":
        autoTimer = random.randrange(4,12)
        setDrive(moveFront)
    else:
        autoTimer = random.randrange(2,6)
        if autoDirection == "LEFT":
            setDrive(moveLeft)
        else:
            setDrive(moveRight)
    message("Moving "+autoDirection+" for "+str(autoTimer)+" seconds")
    return (autoMode,autoTimer)


#
# Moves Drive and Steer servos to stopped/idle position
#
def stopMoving():
    global moveStop
    setDrive(moveStop)
    message("Robot has stopped.")

#
# Setup input section of the form
def inFormSetup(s):
    global moveStop,moveFront,moveLeft,moveRight
    global safeTime,safeDistance
    #
    s.setcolor(s.CYAN,s.BLACK,s.BOLD)
    s.box(1,1,7,60,title="Movement Settings",fill=True)
    s.textat(3,3,"FORWARD")
    s.textat(6,3,"TURNING")
    f = scrnio.form(s)
    f.addHBar("fDrive",2,13,length=12,min=6000,max=7000,delta=100,value=moveFront[0],type="POINT")
    f.addHBar("fSteer",2,29,length=12,min=5500,max=6500,delta=100,value=moveFront[1],type="POINT")
    f.addHBar("tDrive",5,13,length=12,min=6000,max=7000,delta=100,value=moveLeft[0],type="POINT")
    f.addHBar("tLeft" ,5,29,length=12,min=5000,max=6000,delta=100,value=moveLeft[1],type="POINT")
    f.addHBar("tRight",5,45,length=12,min=6000,max=7000,delta=100,value=moveRight[1],type="POINT")
    #
    s.box(9,1,4,43,title="Timing and Distance",fill=True)
    f.addHBar("safeTime",10,5,length=12,min=0,max=5,delta=0.1,value=safeTime)
    f.addHBar("safeDist",10,25,length=12,min=10,max=100,delta=1.0,value=safeDistance)
    #
    s.setcolor(s.MAGENTA,s.BLACK,s.BOLD)
    f.addCheckbox("Autonomous",14,3,"Autonomous")
    f.addButton("Forward",14,23,"Forward")
    f.addButton("Left",15,23,"Left")
    f.addButton("Right",16,23,"Right")
    #
    return f

def inFormProcess(s,f):
    global moveFront,moveLeft,moveRight
    global safeTime,safeDistance
    global autoMode
    #Process any inputs
    key = s.inkey()
    result = f.process(key)
    if result == "Forward":
        startMoving("FRONT")
    elif result == "Left":
        startMoving("LEFT")
    elif result == "Right":
        startMoving("RIGHT")
    elif result != '':  #Any unprocessed keystroke will stop movement 
        stopMoving()
        f.controls("Autonomous").value = False
        f.controls("Autonomous").show()
    #Update Drive and Steer parameters
    moveFront = (f.controls("fDrive").value,f.controls("fSteer").value)
    moveLeft = (f.controls("tDrive").value,f.controls("tLeft").value)
    moveRight = (f.controls("tDrive").value,f.controls("tRight").value)
    #Update timing and distance parameters
    safeTime = f.controls("safeTime").value
    safeDistance = f.controls("safeDist").value
        
            
def outFormSetup(s):
    global safeTime
    f = scrnio.form(s)

    #
    s.box(13,45,10,16,title="Servos",fill=True)
    f.addHBar("sDrive",14,46,length=11,min=5000,max=7000,value=6000,type="POINT")
    f.addHBar("sSteer",17,46,length=11,min=5000,max=7000,value=6000,type="POINT")
    f.addHBar("sScan",20,46,length=11,min=2000,max=9500,value=6000,type="POINT")
    #
    s.box(17,1,6,43,title="Status")
    s.textat(18,3,"Mode")
    s.textat(18,13,"safeTimer")
    s.textat(18,28,"autoTimer")
    s.textat(19,3,"Direction")
    s.textat(19,28,"PIR Dist")
    return f

def outFormProcess(s,f):
    global autoMode,safeTimer,autoTimer,autoDirection,dist
    global servo,servoDrive,servoSteer,servoScanner
    global msgText
    s.textat(18,8,autoMode+" ")
    s.textat(18,23,str(round(safeTimer,1))+ " ")
    s.textat(18,39,str(round(autoTimer,1))+ " ")
    s.textat(19,13,(autoDirection+"       ")[0:8])
    s.textat(19,39,(str(round(dist,0))+ "  ")[0:3])
    s.textat(21,8,(msgText + ' '*30)[0:30])
    #
    f.controls("sDrive").value = servo.getPosition(servoDrive)
    f.controls("sSteer").value = servo.getPosition(servoSteer)
    f.controls("sScan").value = servo.getPosition(servoScanner)
#
# MAIN LOOP
#

#
# Code will continue to run until user presses Ctrl-C
try:
    #
    # Initialize ultrasonic sensor
    sonar = sonic.Sensor()
    #
    # Initialize Servo controller and associated constants
    servo = maestro.Controller()
    # Set Acceleration on Steer and Drive channels
    servo.setAccel(servoSteer,4)
    servo.setAccel(servoDrive,2)
    # Move servos to stop/idle position
    stopMoving()

    #
    # Start out in SCAN mode and wait for it to be safe to move
    (autoMode,autoTimer,autoDirection) = startScanning('')
    safeTimer = safeTime

    #
    # Initialize Screen
    s = scrnio.screen()
    s.cursor(False)
    s.setcolor(s.WHITE,s.BLACK,s.BOLD)
    s.clear()
    fin=inFormSetup(s)
    fin.show()
    #
    s.setcolor(s.GREEN,s.BLACK,s.BOLD)
    fout=outFormSetup(s)
    fout.show()
    #
    s.refresh()
    #
    # Continuous timed loop to process events
    while True:
        #
        # Check PIR distance
        dist = sonar.getDistance()
        if dist < safeDistance:
            objDetected = True
            stopMoving()
            safeTimer = safeTime   #Not safe yet. Start timer over.
        else:
            objDetected = False
        #
        # Process based on current autonomous mode
        if autoMode == "SCAN":
            # Mode is SCAN
            if safeTimer == 0 and fin.controls("Autonomous").value == True:
                # Safe to move now
                (autoMode,autoTimer) = startMoving(autoDirection)
            elif autoTimer == 0:
                # Scanning in current direction done, try scanning some more
                (autoMode,autoTimer,autoDirection) = startScanning(autoDirection)               
        elif autoMode =="MOVE":
            # Mode is MOVE
            if objDetected or autoTimer == 0:
                (autoMode,autoTimer,autoDirection) = startScanning(autoDirection)
        else:  #Mode is STOP
            pass
        #
        # Decrement timers every loop
        autoTimer -= looptime
        if autoTimer < 0 : autoTimer = 0
        safeTimer -= looptime
        if safeTimer < 0 : safeTimer = 0
        
        #
        # Update screen
        inFormProcess(s,fin)
        outFormProcess(s,fout)
        s.refresh()
        #
        # loop delay (keep above 0.10)
        time.sleep(looptime)
    
except KeyboardInterrupt:
    s.close()
    stopMoving()
    setScanner("CENTER")
    servo.close()
    sonar.close()
