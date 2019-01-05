from picamera import PiCamera
from time import sleep
from PIL import Image
from io import BytesIO
import math
import RPi.GPIO as GPIO
import datetime

def servoAngle(angle):
    servoPwm.ChangeDutyCycle(angle)

#Get current system time
time = datetime.datetime.now()

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

composites = dict()

#Sweep servo from 0 to 75.9 degrees
for i in range(759):
    theta = float(i)/10.0
    print("Theta: " + str(theta))
    servoAngle(theta)
##    sleep(.01)

    #Take a picture
    noir.capture(stream, format='jpeg', resize=(759,570))
    stream.seek(0)
    image = Image.open(stream)

    start = i + 115 - 252
    if start < 0:
        start = 0

    end = i + 115
    if end > 759:
        end = 759
    print("Start: " + str(start) + ", End: " + str(end))

    for n in range(start, end):
        phi = n / 10.0
        print ("n: " + str(n))
        strip = image.crop((n,0,n+1,570))
        lamda = int(2000*math.sin(math.radians(11.5 + theta -phi)))
        if not(lamda in composites):
            composites[lamda] = Image.new("RGB", (759, 570))
        composites[lamda].paste(strip,(n,0,n+1,570))

for lamda in composites:
    composites[lamda].save('/home/pi/Pictures/scan' + time.isoformat() + str(lamda) + 'nm.jpg')
    
noir.stop_preview()
