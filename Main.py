import RPi.GPIO as GPIO
import string, subprocess, time, sys, os
from subprocess import call
import LicensePlateRecognition as Lic

print("System Working")

led1=17
led=12
pir=18
HIGH=1
LOW=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)

def matchLicPlate():
    Lic.LicRecognition()
    with open('numberplate.txt','r') as file:
        numberplate = file.read()
    numberlist = ['PB09AC3627', 'KA03MG2825', 'MH08AG7110', 'DL4CAF4943', 'TS08ER1643', 'KA02MJ4606', 'DL8CN8726', 'HR26BF0990', 'HR26BC8009', 'MH12DE1433']
    if numberplate in numberlist:
        GPIO.output(led,HIGH)
        time.sleep(1)
        GPIO.output(led,LOW)
        print(numberplate)

    else:
        print('Number plate not matched!')
        GPIO.output(led,LOW)

def capture_image():
    call(["raspistill -n -t 2000 -o /home/pi/scripts/camera/LicenseImage.jpg -w 2592 -h 1944"], shell=True)
    print("Image Shot")
    p = subprocess.Popen(["runlevel"], stdout=subprocess.PIPE)
    out, err=p.communicate()
    if out[2] == '0':
        print('Halt detected')
        exit(0)
    if out [2] == '6':
        print('Shutdown detected')
        exit(0)
    print("Detecting License Plate")
    matchLicPlate()
    print('----------------------------------------------')

while True:
    if GPIO.input(pir)==1:
        print("Car Movement Detected")
        GPIO.output(led1, HIGH)
        capture_image()
        GPIO.output(led1, LOW)
        GPIO.output(led1, HIGH)
        while(GPIO.input(pir)==1):
            time.sleep(1)

    else:
        GPIO.output(led1, LOW)
        time.sleep(0.01)

GPIO.cleanup()
exit(0)
