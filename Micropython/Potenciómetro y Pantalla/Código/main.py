from machine import Pin, ADC, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep

# ESP32 Pin assignment
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)
poten = ADC(Pin(34))
button = Pin(12, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)

# lista de directorios
# files = os.listdir() 
files = ["lectura_temperatura.py","prender_led.py"]
names = ["calc temp", "use led"]

# Ajustes para el sensor
poten.width(ADC.WIDTH_10BIT) # Regula presición del sensor
poten.atten(ADC.ATTN_11DB) # Trabaja sobre 3.3V

total_lines = 3
width = 128
heigth = 64
line_height = 21


while True:
    lectura = poten.read()

    if 0 <= lectura <= 512:
        oled.fill_rect(1, (0) * line_height, width, line_height, 1) 
        oled.fill_rect(1, (1) * line_height, width, line_height, 0) 
        oled.text("> " + names[0],2,7,0)
        oled.text(names[1],2,28,1)
        function = 0

    if 513 <= lectura <= 1028:
        oled.fill_rect(1, (1) * line_height, width, line_height, 1) 
        oled.fill_rect(1, (0) * line_height, width, line_height, 0) 
        oled.text(names[0],2,7,1)
        oled.text("> " + names[1],2,28,0)
        function = 1

    if button.value() == 0:
        exec(open(files[function]).read())
    
    oled.show()
    led.off()
    sleep(0.05)