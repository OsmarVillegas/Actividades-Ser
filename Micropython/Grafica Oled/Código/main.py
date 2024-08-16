from machine import Pin, ADC, SoftI2C
from utime import sleep_ms
from ssd1306 import SSD1306_I2C
import framebuf
from images import (logo_1,logo_2)

# ESP32 Pin assignment
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)
poten = ADC(Pin(34))

# Ajustes para el sensor
poten.width(ADC.WIDTH_10BIT) # Regula presición del sensor
poten.atten(ADC.ATTN_11DB) # Trabaja sobre 3.3V

WIDTH = 128
HEIGHT = 64
FACTOR = 3.3 / (65535)
    
PLACA = True #True: Raspberry Pi Pico, False: ESP8266
    

buffer = bytearray(logo_2)
    
fb = framebuf.FrameBuffer(buffer,WIDTH,HEIGHT,framebuf.MONO_HLSB)
    
#Global Variables
t = 0
y = [55, 55]
x = [25, 25]
    
oled.fill(0)
oled.text("Control", 35, 0)
oled.text("Automatico", 20, 20)
oled.text("Educacion", 25, 40)
oled.show()
sleep_ms(3000)
    
#Image
oled.fill(0)
oled.blit(fb,0,0)
oled.show()
sleep_ms(3000)
oled.fill(0)
    
def plot_time(yp, t, x, y, var = [0.0,3.3], vpts=[25, 16, 40], hpts = [25, 55, 112]):
    
    #Axis
    oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
    oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
    oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
    oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    #y - axis
    y[1] = int((yp-var[0])/(var[1]-var[0]) * (vpts[1]-hpts[1]) + hpts[1]) #Interpolation
    if t < hpts[2] - hpts[0]:
        x[1] = x[0]+1
    else:
        x[1] = hpts[2]
    
    #Plot the line
    oled.line(x[0],y[0],x[1],y[1],1)
    oled.show()
    
    #Update past values
    y[0] = y[1]
    x[0] = x[1]
    
    #If you have already reached the end of the graph then ...
    if t > hpts[2] - hpts[0]:
        #Erases the first few pixels of the graph and the y-axis.
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0) 
        #Clears the entire y-axis scale
        oled.fill_rect(vpts[0]-25, vpts[1],vpts[0],vpts[2]+5,0)
        #shifts the graph one pixel to the left
        oled.scroll(-1,0)
        #Axis
        oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
        oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
        oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
        oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    else:
        t += 1

    return t,x,y
        
while True:
    volts = poten.read_u16() * FACTOR
    t,x,y = plot_time(volts,t,x,y)
    oled.fill_rect(0,0,120,15,0)
    oled.text("Volts: ", 0, 0)
    oled.text(str(round(volts,1)), 52, 0)
    oled.show()
    sleep_ms(500)
