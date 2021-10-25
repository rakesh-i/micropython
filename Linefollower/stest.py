from machine import Pin, ADC
from time import sleep,time
import motor
sensor = [0, 0, 0, 0]
led = Pin(15, Pin.OUT, Pin.PULL_DOWN)
p1 = Pin(32, Pin.IN)
d1 = Pin(33, Pin.IN)
d2 = Pin(25, Pin.IN) 
sensor[0] = ADC(Pin(35))
sensor[0].atten(ADC.ATTN_11DB)
sensor[1] = ADC(Pin(34))
sensor[1].atten(ADC.ATTN_11DB)
sensor[2] = ADC(Pin(39))
sensor[2].atten(ADC.ATTN_11DB)
sensor[3] = ADC(Pin(36))
sensor[3].atten(ADC.ATTN_11DB)
p6 = Pin(26, Pin.IN)
E1 = Pin(14, Pin.IN)
E2 = Pin(27, Pin.IN)
E3 = Pin(2, Pin.IN)
E4 = Pin(4, Pin.IN)

sens_min = [5000, 5000, 5000 ,5000]
sens_max = [1, 1, 1, 1]
sens_value =[1, 1, 1, 1]
sens_scaled = [1, 1, 1, 1]
RIGHT_DIR =   1
LEFT_DIR =    0 

def test():
    millis = lambda: int(round(time() * 1000))
    max_correction = 100
    last_prop = 0
    integral = 0
    w = 0
    KP = .1
    KD = 1
    KI = .0005
    
    def correction(revolutions):
        if revolutions > 0:
            if revolutions > max_correction:
                revolutions = max_correction
            else:
                revolutions = revolutions
        else:
            if revolutions < -max_correction:
                revolutions = -max_correction
            else:
                revolutions = revolutions 
        return revolutions

    def map(x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    def calibrate(cal_time,  cal_dir):
        ms = millis()
        while((ms+cal_time) > millis()):
            if(cal_dir == RIGHT_DIR):
                pass
                #motor.motorSpeed(-100, 100)
            if(cal_dir == LEFT_DIR):
                pass
                #motor.motorSpeed(100, -100)
                
            for i in range(0, 4):
                sens_value[i] = sensor[i].read()
                if sens_value[i]< sens_min[i]:
                    sens_min[i] = sens_value[i]
                else:
                    sens_min[i] = sens_min[i]
                if sens_value[i]> sens_max[i]:
                    sens_max[i] = sens_value[i]
                else:
                    sens_max[i] = sens_max[i]
        motor.motorSpeed(0,0)

    def r_value():
        global sens_scaled
        for i in range(0,4):
            sens_scaled[i] = sensor[i].read() - sens_min[i]
            sens_scaled[i] *= 1000
            sens_scaled[i] /= (sens_max[i]-sens_min[i])

    def get_line():
        avg_num = 0
        avg_den = 0
        for i in range(0,4):
            r_value()
            avg_num += sens_scaled[i] *i* 1000
            avg_den += sens_scaled[i]
        line = avg_num/avg_den
        line = line - (1000*3/2)
        return line

    while(1):
        calibrate(200, RIGHT_DIR)
        calibrate(200, LEFT_DIR)
        calibrate(200, RIGHT_DIR)
        calibrate(200, LEFT_DIR)
        print(sens_min, sens_max)
        sleep(3)
        while(1):
            
            #print(get_line(), d1.value(), d2.value())
            propotional = get_line()
            derivative = propotional - last_prop
            integral = integral+last_prop
            rotate = (propotional*KP + derivative*KD + integral*KI)
            last_prop = propotional
            r = int(correction(rotate))
            if r < 0:
                motor.motorSpeed(max_correction, max_correction+r )
                
               
            else:
                motor.motorSpeed(max_correction-r, max_correction )
                
                
                
               
            print(r)
            sleep(.1)