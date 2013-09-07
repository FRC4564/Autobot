import time
import RPi.GPIO as GPIO
#
# Distance measurement using the HC-SR04 ultrasonic module
#
# Steven Jacobs -- Aug 2013
#
# Code inspired by Matt Hawkins
#    http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/
#
# Uses GPIO BCM ports 7 and 8 for Echo and Trigger, respectively.
# Use a pair of resistors to divide the 5 volts Echo down to 3.3v for the Pi
#
#    HC-SC04                                 RASPBERRY PI ver. b     
#      Vcc  -------------------------------- +5v    (pin 2)
#
#      Trig -------------------------------- BCM 8  (pin 24)
#
#                       +------------------- BCM 7  (pin 26)
#                       |
#      Echo ----270ohm--+---470ohm-----+ 
#           (red/pur/brn)(yel/pur/brn) |                    
#      Gnd  ---------------------------+---- Gnd    (pin 6)
#
#
# Sample usage:
#
#    import sonic,time
#    s = sonic.Sensor()
#    try:
#       while True:
#           print s.getDistance()
#           time.sleep(.5)
#    except KeyboardInterrupt:
#       s.close()
#
class Sensor:

    #
    # Intialize GPIO and force Trigger low
    #
    def __init__(self):
        # Set GPIO to BCM references
        GPIO.setmode(GPIO.BCM)  
        # Setup GPIO ports
        self.TRIGGER = 8
        self.ECHO = 7
        # 
        GPIO.setup(self.TRIGGER,GPIO.OUT)  # Trigger
        GPIO.setup(self.ECHO,GPIO.IN)      # Echo
        # Initialize trigger to False
        GPIO.output(self.TRIGGER, False)
    #
    # Release GPIO when done
    #
    def close(self):
        GPIO.cleanup()

    #
    # Get distance measurement, in centimeters, from ultra-sonic sensor.
    # Valid measurements will range between 2cm and 150cm with accuracy of +/- 2cm.
    # Values above 150cm should be considered undefined (out of range).
    # Avoid reading the sensor faster than 10 times per second as it may lead to
    # erroneous results.
    #
    def getDistance(self):
        # Send 10us pulse to trigger sensor
        GPIO.output(self.TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, False)
        # Now we'll measure the length of time that Echo line stays high.
        # First, wait for the Echo line to go high and then start timing
        start = time.time()
        maxwait = start + 0.01  #We'll wait no longer then 10ms overall
        while GPIO.input(self.ECHO) == 0 and start < maxwait:
            start = time.time()
        # Now we'll wait for the Echo line to go low and measure the end time.
        # If no objects in range, it could take quite a while for
        # the echo (about 0.125secs).  We'll wait long enough to
        # measure distances to about 1.2meters (about .007secs), so as not
        # to waste CPU time waiting around.
        stop = time.time()
        while GPIO.input(self.ECHO) == 1 and stop < maxwait:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start
        # Distance pulse travelled is the elapsed time
        # multiplied by the speed of sound (cm/s)
        # and then halfed, since sound travelled back and forth.
        distance = elapsed * 34300 / 2
        # return the distance with an adder to calibrate for improved accuracy
        # adjust the factor for your particular sensor/Pi combination
        return distance + 1.2
