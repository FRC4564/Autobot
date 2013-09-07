import scrnio
import math
import time
import maestro

# Init servo controller
SteerStop=5000
DriveStop=5000
servo = maestro.Controller()


# embed entire scrnio process in a try/except block
try:
    #
    # SCREEN SETUP
    #
    s = scrnio.screen()
    s.cursor(False)
    s.setcolor(s.CYAN,s.BLACK,s.BOLD)
    s.clear()
    s.textat(1,1,'AutoBot')
    s.setcolor(s.WHITE,s.RED,s.BOLD)
    s.textat(1,15,'Press any letter key for emergency halt')

    #Input controls form
    inp = scrnio.form(s)
    s.setcolor(s.CYAN,s.BLUE,s.BOLD)
    inp.addCheckbox("Enable",3,3,"Enable Control")
    inp.addHBar("Steer",5,3,length=23,min=1200,max=9000,value=SteerStop,delta=100,type='POINT')
    inp.addHBar("Drive",5,30,length=23,min=1200,max=9000,value=DriveStop,delta=100,type='POINT')
    inp.addHBar("SAccel",9,3,length=10,min=0,max=50,value=5,delta=1,type='FILL')
    inp.addHBar("SSpeed",9,16,length=10,min=0,max=50,value=5,delta=1,type='FILL')
    inp.addHBar("DAccel",9,30,length=10,min=0,max=50,value=5,delta=1,type='FILL')
    inp.addHBar("DSpeed",9,43,length=10,min=0,max=50,value=5,delta=1,type='FILL')
#    inp.addButton("btnSNeutral",3,55,"Stop")
#    inp.addButton("btnDNeutral",7,55,"Stop")

#    s.setcolor(s.CYAN,s.RED,s.BOLD)
#    inp.addButton("Exit",11,28,"Exit",width=10)

    inp.select("Enable")
    inp.show()

    # Output fields
    s.setcolor(s.WHITE,s.MAGENTA,s.BOLD)
    out = scrnio.form(s)
    out.addHBar("SteerPos",13,3,length=23,min=1500,max=9000,value=5000,type='POINT')
    out.addHBar("DrivePos",13,30,length=23,min=1500,max=9000,value=5000,type='POINT')
    out.show()

    # Prep for main loop
    fps = 30
    delay = 1.0 / fps 
    t = time.time() + delay
    
    done = False
    while not done:

        # process key input
        key=s.inkey()
        if key != '':           
            result = inp.process(key)
            #Any key not processed by the form will cause the loop exit (emergency stop)
            if result != '':
                done = True

        # update servos
        if inp.controls('Enable').value:
            servo.setAccel(0,inp.controls('SAccel').value)
            servo.setSpeed(0,inp.controls('SSpeed').value)
            servo.setTarget(0,inp.controls('Steer').value)
            servo.setAccel(1,inp.controls('DAccel').value)
            servo.setSpeed(1,inp.controls('DSpeed').value)
            servo.setTarget(1,inp.controls('Drive').value)
        else:
            servo.setTarget(0,SteerStop)
            servo.setTarget(1,DriveStop)
                
        # show the output fields and refresh the screen
        out.controls('SteerPos').value = servo.getPosition(0)
        out.controls('DrivePos').value = servo.getPosition(1)
        out.show()
        
        s.refresh()

        # pace loop based on FPS delay
        while time.time() < t:
            s.wait(10)
        t = t + delay

    # Close out the Forms and Screen    
    s.close()
    servo.setSpeed(0,0)
    servo.setSpeed(1,0)
    servo.setTarget(0,SteerStop)
    servo.setTarget(1,DriveStop)
    servo.close()
    print result,key
except:    
    s.close()
    servo.setSpeed(0,0)
    servo.setSpeed(1,0)
    servo.setTarget(0,SteerStop)
    servo.setTarget(1,DriveStop)
    servo.close()
    raise
