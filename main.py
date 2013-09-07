import time
import random
#<< IMPORT BOTH THE 'maestro' AND 'sonic' PYTHON CLASSES>>
<<>>
#--------------------------
# CONSTANTS AND VARIABLES
#--------------------------

# Servo channel assignment constants
servoSteer=0     #steering
servoDrive=1     #motor drive
#<< CREATE A CONSTANT FOR servoScanner SETUP AS CHANNEL 5>>
<<>>

# Drive and Steering parameter pair constants
driveStop    = (5800,6000)   #Stop forward motion and Steer straight
driveFront   = (10500,6000)  #Move forward and Steer straight
#<< CREATE CONSTANTS FOR driveLeft AND driveRight. SETUP WITH NO FORWARD MOTION AND STEERING
#<< OF 8000 FOR LEFT AND 4000 FOR RIGHT >>
<<>>

# Define autonomous movement variables
#<< SET AUTONOMOUS MODE TO SCAN. HINT: READ THE COMMENT LINE.>>
autoMode = <<>>      #Autonomus mode is either "SCAN" or "MOVE".
autoTimer = 0        #Timer in seconds for how long current autoMode is to run.
autoDirection = ""   #Direction automous mode is either Scanning and/or Moving - "FORWARD", "LEFT", "RIGHT"

# Sonar safe distance constants and variable
#<< SETUP safeDistance CONSTANT TO 40 CENTIMETERS>>
<<>>                 #Minimum safe distance in centimeters
#<< SETUP safeTime CONSTANT AT 1 SECOND
<<>>                 #Number of seconds required, without object detection, to be consider safe to move.
safeTimer = safeTime #Timer will start at SafeTime and counts down to 0, if no obstacles seen.

# Main Loop delay. Keep delay 0.1secs or higher, so as to not overwhelm sonar. 
#<< PROIVDE A looptime CONSTANT TO PROCESS AT 5 TIMES PER SECOND.  PAY ATTENTION TO THE UNITS.
looptime=<<>>        #Seconds of delay between main loop cycles

#------------
# FUNCTIONS
#------------

# Randomly returns one of three directions LEFT, RIGHT, or FRONT as a string.
# FRONT is twice as likely as LEFT or RIGHT.
def rndDirection():
    <<BUILD THE CODE TO RETURN A Direction AS NOTED IN THE COMMENT ABOVE>>
    <<HINT: SEE beachbot.py FOR SYNTAX ON GENERATING A RANDOM NUMBER>>
    return Direction

# Set scanner to scan in the direction indicated.  This uses Maestro scripts 
# to perform the osciliation of the servo.  Directions are "LEFT", "RIGHT", and "FRONT.
# A special case, "CENTER", points sensor straight-ahead and halts oscilations.  
def setScanner(direction):
    # Script subroutines are numbered 0 through 3 on the Maestro
    Subs = {"CENTER":0,"FRONT":1,"LEFT":2,"RIGHT":3}
    #<< USING Subs AND THE direction PARAMETER, OBTAIN THE SubNumber. HINT: SQUARE BRACKETS>>
    SubNumber = <<>>
    #<< CALL THE MAESTRO FUNCTION THAT WILL RUN THE SCRIPT SUBROUTINE SubNumber>>
    servo.<<>>

#
# Randomly select a direcion to scan which will be where we move next, if safe.
# Returns: autoMode='SCAN', autoTimer=5, autoDirection={random direction} 
#
def startScanning(currDirection):
    autoMode = "SCAN"
    autoTimer = 5   #Set time so that Scan will wait no more than 5secs before scanning in another direction
    #<< DETERMINE A RANDOM DIRECTION TO SCAN.  HINT: YOU'VE ALREADY DONE THE HARD WORK.>>
    autoDirection = <<>>
    # If this is a different direction than current, set the scanner to the new direction
    #<< WRITE THE if STATEMENT THE WILL PERFORM THE TEST NOTED ABOVE.  HINT: != IS NOT EQUALS>>
    if <<>>
        #<< CALL THE setScanner FUNCTION FOR THE NEW DIRECTION>>
        <<>>
    print "Scanning ",autoDirection," for up to",autoTimer," seconds."
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
    #<< SET THE STEERING SERVO BASED ON THE targets STEER PARAMETER, JUST LIKE THE TWO LINES ABOVE>>
    <<>>

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
        #<< WRITE CODE TO SET autoTimer RANDOMLY BETWEEN 2 AND 6 SECONDS AND THEN setDrive >>
        #<< ACCORDINGLY WITH THE DIRECTION OF MOVEMENT, LEFT OR RIGHT>>
        <<>>
    print "Robot now moving ",autoDirection," for ",autoTimer," seconds"
    return (autoMode,autoTimer)


#
# Moves Drive and Steer servos to stopped/idle position
#
def stopMoving():
    global driveStop
    ##<< STOP ROBOT MOVEMENT>>
    <<>>
    print "Robot has stopped."

#
# MAIN LOOP
#

#
# Code will continue to run until user presses Ctrl-C
try:
    #
    # Initialize ultrasonic sensor
    ##<< INITIALIZE THE SENSOR.  HINT: REFER TO sonic.py FOR SAMPLE USAGE>>
    sonar = <<>>
    #
    # Initialize Servo controller and associated constants
    ##<< INITIALIZE THE MAESTRO CONTROLLER.>>
    servo = <<>>
    # Set Acceleration on Steer and Drive channels
    ##<< SET ACCELLERATION OF THE STEERING SERVO TO 4>>
    servo.setAccel(servoSteer,<<>>)
    ##<< SET ACCELERATION OF THE DRIVE SERVO TO 2>>
    <<>>
    # Move servos to stop/idle position
    ##<<HINT: YOU HAVE A FUNCTION FOR THIS>>
    <<>>
    #
    # Start out in SCAN mode and wait for it to be safe to move
    (autoMode,autoTimer,autoDirection) = startScanning('')
    ##<< INIT THE safeTimer. THERE IS A CONSTANT FOR WHAT THIS SHOULD START AT>> 
    <<>>
    #
    # Continuous timed loop to process events
    while True:
        dist = sonar.getDistance()
        ##<< COMPLETE THE if TO TEST IF AN OBJECT IS TOO CLOSE. HINT: LOOK AT THE CONTANTS.>>
        if <<>>:
            objDetected = True
            ##<< STOP MOVEMENT>>
            <<>>
            ##<< RESET THE safeTimer TO START OVER >>
            <<>>   #Not safe yet. Start timer over.
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
