import machine
from machine import Pin, PWM
import time

#pin definition
p1 = machine.Pin(19, machine.Pin.OUT)
p2 = machine.Pin(18, machine.Pin.OUT)
p3 = machine.Pin(5)
pwm1 = machine.PWM(p3, freq=50)
p4 = machine.Pin(22, machine.Pin.OUT)
p5 = machine.Pin(21, machine.Pin.OUT)
p6 = machine.Pin(23)
pwm2 = machine.PWM(p6, freq=50)

#arduino "map" function implementation
def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

#easy to use function for setting motor speed and direction
def motorSpeed(m1, m2):
    pw1 = convert(abs(m1),0, 1000, 0, 1000) 
    pw2 = convert(abs(m2),0, 1000, 0, 1000)
    pwm1.duty(pw1)
    pwm2.duty(pw2)
    p1.on() if m1>0 else p1.off()
    p2.off() if m1>0 else p2.on()
    p4.on() if m2>0 else p4.off()
    p5.off() if m2>0 else p5.on()




