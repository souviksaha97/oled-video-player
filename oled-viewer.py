import cv2
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import numpy as np
import time

WIDTH = 128
HEIGHT = 64 # Change to 32 depending on your screen resolution

cap = cv2.VideoCapture('vid2.webm') #Enter the name of your video in here
oled_reset = digitalio.DigitalInOut(board.D4)

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)

image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
frameCounter = 0
frameSkip = 1 #Change to adjust frame rate
lowerThresh = 0# Adjust threshold according to video
while(cap.isOpened()):
    ret, frame = cap.read()
    frameStart = time.time()
    if ret==True:
        if frameCounter%frameSkip == 0:
            # Import image as grayscale
##            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(frame, (oled.width, oled.height))

            # Resize to fit OLED screen dimensions
##            resized = cv2.resize(gray, (oled.width, oled.height))
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            # Threshold it to B&W
            (thresh, bw) = cv2.threshold(gray, lowerThresh, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            # Clear screen for next frame
            draw.rectangle((0, 0, oled.width, oled.height),
                       outline=0, fill=0)
##            oled.fill(0)
            # Convert to OLED format, and print
            screenframe = Image.fromarray(bw).convert("1")
            oled.image(screenframe)
            oled.show()
            frameEnd = time.time()
            print(1/(frameEnd-frameStart))
        frameCounter=frameCounter+1
