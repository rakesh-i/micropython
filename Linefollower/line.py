from machine import Pin, ADC
from time import sleep
import motor

path = []
path_length = 0
total_angle = 0

l_flag = 0
r_flag = 0

sensor_read = [0, 0, 0, 0]
sensor = [0, 0, 0, 0]
led = Pin(15, Pin.OUT, Pin.PULL_DOWN)
p1 = Pin(25, Pin.IN)
sensor[0] = ADC(Pin(35))
sensor[0].atten(ADC.ATTN_11DB)
sensor[1] = ADC(Pin(34))
sensor[1].atten(ADC.ATTN_11DB)
sensor[2] = ADC(Pin(39))
sensor[2].atten(ADC.ATTN_11DB)
sensor[3] = ADC(Pin(36))
sensor[3].atten(ADC.ATTN_11DB)
p6 = Pin(33, Pin.IN)

E1 = Pin(14, Pin.IN)
E2 = Pin(27, Pin.IN)
E3 = Pin(13, Pin.IN)
E4 = Pin(12, Pin.IN)

def r_value():
    for i in range(0,4):
        sensor_read[i] = sensor[i].read()

def get_line():
    avg_num = 0
    avg_den = 0
    for i in range(0,4):
        r_value()
        avg_num += sensor_read[i] *i* 1000
        avg_den += sensor_read[i]
    line = avg_num/avg_den
    line = line - (1000*3/2)
    return line,avg_den,avg_num

while(1):
    r_value()
    
    if sensor_read[0]>2000 and sensor_read[3] < 2000:
        motor.motorSpeed(100, -100)
    if sensor_read[0]<2000 and sensor_read[3] > 2000:
        motor.motorSpeed(-100,100)
    if sensor_read[0]<2000 and sensor_read[3] < 2000:
        motor.motorSpeed(100, 100)
    print(sensor_read[1], sensor_read[2])
    sleep(.1)