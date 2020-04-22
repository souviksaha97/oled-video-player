import cv2
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import numpy as np
import time

WIDTH = 128
HEIGHT = 64
# Change to 64 if needed
BORDER = 5
cap = cv2.VideoCapture('vid1.mp4')
oled_reset = digitalio.DigitalInOut(board.D4)
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)

image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
frameCounter = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        if frameCounter%10==0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (oled.width, oled.height))
            (thresh, bw) = cv2.threshold(resized, 240, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
##            bw = cv2.Canny(resized,100,200)

    ##        print('frame')
            draw.rectangle((0, 0, oled.width, oled.height),
                       outline=0, fill=0)
##            image = cv2.resize(bw, (oled.width, oled.height))
##            cv2.imwrite("frame.jpg", bw)
    ##        cv2.imshow('frame', image)
    ##        
    ##        if cv2.waitKey(1) & 0xFF == ord('q'):
    ##            break
    ##
    ##cap.release()
    ##cv2.destroyAllWindows()
            screenframe = Image.fromarray(bw).convert("1")
    ##        print(type(screenframe))
            oled.image(screenframe)
            oled.show()
    ##        time.sleep(0.011)
        frameCounter=frameCounter+1
