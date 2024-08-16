import dht

sensor = dht.DHT22(Pin(14))

oled.fill_rect(1, (0) * line_height, width, line_height, 0) 
oled.fill_rect(1, (1) * line_height, width, line_height, 0) 


sensor.measure()
data = sensor.temperature()

oled.text(str(data),0,0)
