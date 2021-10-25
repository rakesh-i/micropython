from machine import Pin
import time
#import motor

p1 = Pin(14, Pin.IN)
p2 = Pin(27, Pin.IN)
p3 = Pin(13, Pin.IN)
p4 = Pin(12, Pin.IN)

pos1 = 0
pos2 = 0 



#Swap encoder pins if pos(position counter) value doesn't reduce when we reverse the direction of motor.
def handle_interrupt1(pin):
    global pos1
    a = p1.value()
    if a > 0:
        pos1 = pos1+1
        #print("hello")
    else:
        pos1 = pos1-1

def handle_interrupt2(pin):
    global pos2
    a = p3.value()
    if a>0:
        pos2 = pos2+1
        #print("hello")
    else:
        pos2 = pos2-1
        #print("bey")


p4.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt2)
p2.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt1)


 

while(1):
    print(pos1, pos2)
    time.sleep(.1) 