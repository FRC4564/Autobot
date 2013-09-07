import scrnio
import math
import time
import maestro

servo = maestro.Controller()



try:

    s = scrnio.screen()
    s.cursor(False)
    s.setcolor(s.CYAN,s.BLACK,s.BOLD)
    s.clear()
    s.textat(1,1,'AutoBot testing')

    #Input form
    f = scrnio.form(s)
    s.setcolor(s.CYAN,s.BLUE,s.BOLD)
    f.addHBar("Min",3,5,40,1200,5100,3000,delta = 100,type='POINT')
    f.addHBar("Max",7,5,40,5100,9000,6000,delta = 100,type='POINT')
    f.addCheckbox("On",12,5,"Enable Servo")
    f.addHBar("Rate",14,5,10,.01,.1,.03,delta = .01,type='FILL')

    s.setcolor(s.CYAN,s.RED,s.BOLD)
    f.addButton("Exit",4,52,"Exit",width=10)
    f.select("Min")
    f.show()

    # Output form
    fout = scrnio.form(s)
    s.setcolor(s.WHITE,s.MAGENTA,s.BOLD)
    fout.addHBar("Oscillator",14,19,length=26,min=-1,max=1,value=0,type='POINT')
    fout.show()

    # Prep for main loop
    fps = 30
    delay = 1.0 / fps 
    t = time.time() + delay
    
    oscillator = 0

  
    done = False
    while not done:

        # process key input
        key=s.inkey()
        if key != '':           
            result = f.process(key)
            if result != '':
                done = True

        # update oscilator
        oscillator += f.controls('Rate').value
        amplitude = math.sin(oscillator)
        fout.controls('Oscillator').value = round(amplitude,2)

        # update servo relative to oscillator
        if f.controls('On').value:
            min = f.controls('Min').value
            max = f.controls('Max').value
            range = max - min
            midrange = range / 2
            midpoint = range / 2 + min
            servo.setTarget(5,int(midrange * amplitude + midpoint))
                
        # show the output fields and refresh the form
        fout.show()
        s.refresh()

        # throttle loop based on FPS delay
        while time.time() < t:
            s.wait(10)
        t = t + delay

    # Close out the Froms and Screen    
    s.close()
    servo.close()
    print result,key
except:    
    s.close()
    servo.close()
    raise
