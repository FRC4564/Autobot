import time
import maestro
import sonic
import random

#--------------------------
# CONSTANTS AND VARIABLES
#--------------------------

# Servo channel assignment constants
servoSteer=0     #steering
servoDrive=1     #motor drive
servoScanner=5   #sonar scanner

# Drive and Steering parameter pair constants
driveStop    = (5800,6000)   #Stop forward motion and Steer straight
driveFront   = (10500,6000)  #Move forward and Steer straight
driveLeft    = (5800,8000)   #Stop forward motion and Steer left
driveRight   = (5800,4000)   #Stop forward motion and Steer right

# Define autonomous movement variables
autoMode = ""        #Autonomus mode is either "SCAN" or "MOVE".
autoTimer = 0        #Timer in seconds for how long current autoMode is to run.
autoDirection = ""   #Direction automous mode is either Scanning and/or Moving - "FORWARD", "LEFT", "RIGHT"

# Sonar safe distance constants and variable
safeDistance = 40    #Minimum safe distance in centimeters
safeTime = 1         #Number of seconds required, without object detection, to be consider safe to move.
safeTimer = safeTime #Timer will start at SafeTime and counts down to 0, if no obstacles seen.

# Main Loop delay. Keep delay 0.1secs or higher, so as to not overwhelm sonar. 
looptime=0.2         #Seconds of delay between main loop cycles

#------------
# FUNCTIONS
#------------

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
    print "Scanning ",autoDirection," for ",autoTimer," up to seconds."
    return (autoMode,autoTimer,autoDirection)    

#
# Set drive servos to target positions measured in 1/4 micro-second pulse widths.
# Pass 'targets' paramaeter in the format (drivetarget,steertarget).
# Use the constants 'driveStop', 'driveFront', and so on as the parameter.
#
def setDrive(targets):
    global servoDrive, servoSteer
    servo.setTarget(servoDrive,targets[0])
    print "Drive",servoDrive,targets[0]
    servo.setTarget(servoSteer,targets[1])
    print "Steer",servoSteer,targets[1]

#
# Once it has been determined it is safe to move, calling this subroutine
# will set the automous mode to MOVE, pick a random direction to move, determine
# a random time to move in that direction, and issue set the servos in motion.
#
def startMoving(autoDirection):
    global driveFront,driveLeft,driveRight
    autoMode = "MOVE"
    if autoDirection == "FRONT":
        autoTimer = random.randrange(4,12)
        setDrive(driveFront)
    else:
        autoTimer = random.randrange(2,6)
        if autoDirection == "LEFT":
            setDrive(driveLeft)
        else:
            setDrive(driveRight)
    print "Robot now moving ",autoDirection," for ",autoTimer," seconds"
    return (autoMode,autoTimer)


#
# Moves Drive and Steer servos to stopped/idle position
#
def stopMoving():
    global driveStop
    setDrive(driveStop)
    print "Robot has stopped."

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
    # Continuous timed loop to process events
    while True:
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
            if safeTimer <= 0:
                # Safe to move now
                (autoMode,autoTimer) = startMoving(autoDirection)
            elif autoTimer <= 0:
                # Scanning in current direction done, try scanning some more
                (autoMode,autoTimer,autoDirection) = startScanning(autoDirection)               
        else:
            # Mode is MOVE
            if objDetected or autoTimer <= 0:
                (autoMode,autoTimer,autoDirection) = startScanning(autoDirection)
        #
        # Decrement timers every loop
        autoTimer -= looptime
        safeTimer -= looptime
        #
        # loop delay (keep above 0.10)
        time.sleep(looptime)

except KeyboardInterrupt:
    stopMoving()
    setScanner("CENTER")
    servo.close()
    sonar.close()
