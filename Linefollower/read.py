from machine import Pin, ADC
from time import sleep,time
import motor
millis = lambda: int(round(time() * 1000))

path =[]
path_length =0
l_flag = 0
r_flag = 0
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
E3 = Pin(13, Pin.IN)
E4 = Pin(12, Pin.IN)

pos1 = 0
pos2 = 0 
def re():
    global sensor
    global r_flag
    global l_flag
    global path_length 
    sens_scaled = [0, 0, 0, 0]
    RIGHT_DIR =   1
    LEFT_DIR =    0 
    global path 
    sens_min = [5000, 5000, 5000 ,5000]
    sens_max = [1, 1, 1, 1]
    sens_value =[1, 1, 1, 1]
    sens_scaled = [1, 1, 1, 1]
    
    
    #Map function to map values to certain range
    def map(x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    def calibrate(cal_time, cal_speed, cal_dir):
        ms = millis()
        while((ms+cal_time) > millis()):
            if(cal_dir == RIGHT_DIR):
                print("turning right")
            if(cal_dir == LEFT_DIR):
                print("turning left")
            
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
                print(sens_value[i], sens_min[i], sens_max[i])   
            sleep(.01)

        

    #Swap encoder pins if pos(position counter) value doesn't reduce when we reverse the direction of motor.
    def handle_interrupt1(pin):
        global pos1
        a = E1.value()
        if a > 0:
            pos1 = pos1+1
        else:
            pos1 = pos1-1

    def handle_interrupt2(pin):
        global pos2
        a = E3.value()
        if a>0:
            pos2 = pos2+1
            #print(a)
        else:
            pos2 = pos2-1
            #print(0)

    E4.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt2)
    E2.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt1)

    def r_value():
        for i in range(0,4):
            sens_scaled[i] = sensor[i].read() - sens_min[i]
            sens_scaled[i] *= 4000
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
        return line,avg_den,avg_num

    def turn(dir):
        global l_flag
        global r_flag
        #print("hello")
        #sleep(1)
        #print("bey")
        if dir == "L":
            print("Turning left")
            sleep(1)
        elif dir == "S":
            print("Straight")
            sleep(1)
        elif dir == "R":
            print("Turning right")
            sleep(1)
        else:
            print("U turn")
            sleep(1)
        l_flag =0
        r_flag =0
        

    def left(pin):
        sleep(.2)
        global l_flag
        global r_flag
        l_flag = 1
        if r_flag ==1:
            r_flag =0

    def right(pin):
        sleep(.2)
        global r_flag
        r_flag = 1
        if l_flag ==1:
            r_flag = 0

    def tot(argument):
        global total_angle
        if argument == "R":
            total_angle += 90
        elif argument == "L":
            total_angle += 270
        elif argument == "B":
            total_angle += 180
        else:
            total_angle +=0
            

    def angle(argument):
            if argument == 0:
                path[path_length-3] = "S"
            elif argument == 90:
                path[path_length-3] = "R"
            elif argument == 180:
                path[path_length-3] = "B"
            elif argument == 270:
                path[path_length-3] = "L"

    def simplify_path():
        global path_length
        global total_angle 
        global path
        total_angle = 0
        print(path_length)
        print(path)
        #print(path[1])
        if path_length<3 or path[path_length-2] != "B":
            
            

            

            return
        for i in range(1,4):
            tot(path[path_length-i])
            #print(path[path_length-i], total_angle)
        total_angle = total_angle%360
        angle(total_angle)
        path.pop()
        path.pop()
        path_length -=2

    p1.irq(trigger=Pin.IRQ_RISING, handler=left)
    p6.irq(trigger=Pin.IRQ_RISING, handler=right)
    
    def race():
        global path_length
        global sensor
        global r_flag
        global l_flag
        
        
        while(1):
            r_value()
            if sens_scaled[0]<1000 and sens_scaled[1]<1000 and sens_scaled[2]<1000 and sens_scaled[3]<2000:
                sleep(.5)
                #print("u_turn")
                path.append("B")
                #print(path)
                path_length+= 1
                simplify_path()
                turn("B")
            elif l_flag == 1:
                sleep(.3)
                if sens_scaled[0]>2000 and sens_scaled[1]>2000 and sens_scaled[2]>2000 and sens_scaled[3]>2000:
                    print("end")
                    break
                #print("left")
                path.append("L")
                path_length+= 1
                simplify_path()
                l_flag = 0
                turn("L")
            elif r_flag == 1:
                sleep(.3)
                if sens_scaled[1]>1500 and sens_scaled[2]>1500:
                    #print("straight")
                    path.append("S")
                    path_length+= 1
                    simplify_path()
                    r_flag = 0
                    turn("S")
                elif r_flag == 1:
                    #print("right")
                    path.append("R")
                    path_length+= 1
                    simplify_path()
                    r_flag = 0
                    turn("R")
            #for i in range(0,3):
            
            print(sens_scaled[0],sens_scaled[1], sens_scaled[2], sens_scaled[3], pos1, pos2)
            #print(get_line())
            sleep(.01)
        while(1):
            led.value(1)
            sleep(5)
            led.value(0)
            print(path)

    while(1):
        global path
        calibrate(500, 50, RIGHT_DIR)
        calibrate(500, 50, LEFT_DIR)
        calibrate(500, 50, RIGHT_DIR)
        calibrate(500, 50, RIGHT_DIR)
        
        print("calibarted")
        print(sens_max, sens_min)
        sleep(5)
        race()
        
        
        


