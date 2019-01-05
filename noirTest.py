from picamera import PiCamera
from time import sleep
from PIL import Image
from io import BytesIO
import os
import math
import RPi.GPIO as GPIO
import datetime

def servoAngle(angle):
    servoPwm.ChangeDutyCycle(angle)

#Get current system time
time = datetime.datetime.now()

os.mkdir('/home/pi/Pictures/scan' + time.isoformat())

d = 2000.0          #spacing between diffraction grating in nm
lambda0 = 400.0     #minimum wavelength of interest in nm
lambda1 = 900.0     #maximum wavelength of interest in nm
phiMax = 62.2       #camera's field of view
stepAngle = .5      #angular resolution of servo

#Angle of minimum wavelength of interest from theta = 0 in degrees
theta0 = degrees(math.asin(lambda0/d))

#Angle of maximum wavelength of interest from theta = 0 in degrees
theta1 = degrees(math.asin(lambda1/d))

#Maximum servo angle
thetaMax = phiMax + theta1

#Minimum servo angle
thetaMin = 0.0 + theta0

xres = 3280     #the raw resolution of the camera
yres = 2464

rat  = yres / xres  #the aspect ratio

xadj = phiMax/stepAngle
yadj = phiMax/stepAngle * rat

#Set up servo pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
servoPwm = GPIO.PWM(18, 50)
servoPwm.start(0)

#Set up 'in-memory' stream
stream = BytesIO()

#Set up camera
noir = PiCamera()
##noir.resolution(3280, 2464)

#Set servo to home position
servoAngle(0)

#Start camera
noir.start_preview()
sleep(5)
#camera.color_effects = (128,128) #Monochrome mode
noir.exposure_mode = 'off'

composites = dict() #empty dictionary to contain hyperspectral cube

#Sweep servo from thetaMin to thetaMax degrees
for theta in range(thetaMin, thetaMax, stepAngle)
    print("Theta: " + str(theta))

    #Set servo to current theta
    servoAngle(theta)
##    sleep(.01)

    #Take a picture
    noir.capture(stream, format='jpeg', resize=(xadj, yadj))
    stream.seek(0)
    image = Image.open(stream)  #Turn the stream into a PIL Image object
    stream.seek(0)

    #limits for interesting phi
    startPhi = theta - theta1
    if startPhi < 0:
        startPhi = 0
    endPhi = theta - theta0
    if endPhi > phiMax:
        endPhi = phiMax
        
    print("Start: " + str(startPhi) + ", End: " + str(endPhi))

    for phi in range(startPhi, endPhi, stepAngle):
        
        print ("Phi: " + str(phi))
        col = int(phi/stepAngle)    #column of interest
        strip = image.crop((col, 0, col + 1, yadj))

        #the wavelength
         lamda = int(d * math.sin(math.radians(theta - phi)))
        if not(lamda in composites):
            composites[lamda] = Image.new("RGB", (xadj, yadj))
        composites[lamda].paste(strip,(col, 0, col+1,yadj))

for lamda in composites:
    composites[lamda].save('/home/pi/Pictures/scan' + time.isoformat() + '/' + str(lamda) + 'nm.jpg')
    
noir.stop_preview()
