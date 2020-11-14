import RPi.GPIO as GPIO
import time
import string

#
run_car  = '1'  #
back_car = '2'  #
left_car = '3'  #
right_car = '4' #
stop_car = '0'  #

#
front_left_servo = '1'  #
front_right_servo = '2' #
up_servo = '3'          #
down_servo = '4'        #
left_servo = '6'        #
right_servo = '7'       #
updowninit_servo = '5'  #
stop_servo = '8'        #

#
enSTOP = 0
enRUN =1
enBACK = 2
enLEFT = 3
enRIGHT = 4
enTLEFT =5
enTRIGHT = 6

#
enFRONTSERVOLEFT = 1
enFRONTSERVORIGHT = 2
enSERVOUP = 3
enSERVODOWN = 4
enSERVOUPDOWNINIT = 5
enSERVOLEFT = 6
enSERVORIGHT = 7
enSERVOSTOP = 8



#
ServoLeftRightPos = 90
ServoUpDownPos = 90
g_frontServoPos = 90
g_nowfrontPos = 0


#
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#
key = 8

#
EchoPin = 0
TrigPin = 1

#
LED_R = 22
LED_G = 27
LED_B = 24 

#
FrontServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11

# 
AvoidSensorLeft = 12
AvoidSensorRight = 17

#
buzzer = 8

#
OutfirePin = 2

#

TrackSensorLeftPin1  =  3   #
TrackSensorLeftPin2  =  5   #
TrackSensorRightPin1 =  4   #
TrackSensorRightPin2 =  18  #

#
LdrSensorLeft = 7
LdrSensorRight = 6

#
#
red = 0
green = 0
blue = 0
#
NewLineReceived = 0
InputString = ''
recvbuf = ''
ReturnTemp = ''
#
g_CarState = 0
g_ServoState = 0
#
CarSpeedControl = 80 
#
infrared_track_value = ''
infrared_avoid_value = ''
LDR_value = ''
g_lednum = 0


def action(action,args):
    pass

def get_sensor_list():
    pass

def get_sensor(sensor_id):
    pass
    
def get_state():
    pass


def init():
    #
    GPIO.setmode(GPIO.BCM)
    #
    GPIO.setwarnings(False)
    global pwm_ENA
    global pwm_ENB
    global pwm_FrontServo
    global pwm_UpDownServo
    global pwm_LeftRightServo
    global pwm_rled
    global pwm_gled
    global pwm_bled
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(OutfirePin,GPIO.OUT)
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.setup(FrontServoPin, GPIO.OUT)
    GPIO.setup(ServoUpDownPin, GPIO.OUT)
    GPIO.setup(ServoLeftRightPin, GPIO.OUT)
    GPIO.setup(AvoidSensorLeft,GPIO.IN)
    GPIO.setup(AvoidSensorRight,GPIO.IN)
    GPIO.setup(LdrSensorLeft,GPIO.IN)
    GPIO.setup(LdrSensorRight,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN)
    #
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #
    pwm_FrontServo = GPIO.PWM(FrontServoPin, 50)
    pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
    pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
    pwm_FrontServo.start(0)
    pwm_UpDownServo.start(0)
    pwm_LeftRightServo.start(0)
    pwm_rled = GPIO.PWM(LED_R, 1000)
    pwm_gled = GPIO.PWM(LED_G, 1000)
    pwm_bled = GPIO.PWM(LED_B, 1000)
    pwm_rled.start(0)
    pwm_gled.start(0)
    pwm_bled.start(0)
	
#	
def run():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#
def back():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
	
#	
def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#
def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
	
#
def spin_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

#	
def brake():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)
				
#
def Distance_test():
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
        t1 = time.time()
    while GPIO.input(EchoPin):
        pass
        t2 = time.time()
    print ("distance is %d " % (((t2 - t1)* 340 / 2) * 100))
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100
	
#
def frontservo_appointed_detection(pos): 
    for _ in range(18):   
    	pwm_FrontServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.02)							#
    	#pwm_FrontServo.ChangeDutyCycle(0)	#

#
def leftrightservo_appointed_detection(pos): 
    for _ in range(1):   
    	pwm_LeftRightServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.02)							#
    	#pwm_LeftRightServo.ChangeDutyCycle(0)	#

#
def updownservo_appointed_detection(pos):  
    for _ in range(1):  
    	pwm_UpDownServo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.02)							#
    	#pwm_UpDownServo.ChangeDutyCycle(0)	#

#
def whistle():
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.001)	

#
def color_led_pwm(iRed,iGreen,iBlue):
    v_red = (100*iRed)/255
    v_green = (100*iGreen)/255
    v_blue = (100*iBlue)/255
    pwm_rled.ChangeDutyCycle(v_red)
    pwm_gled.ChangeDutyCycle(v_green)
    pwm_bled.ChangeDutyCycle(v_blue)
    time.sleep(0.02)

#
def servo_up():
    global ServoUpDownPos
    pos = ServoUpDownPos
    updownservo_appointed_detection(pos)
    #time.sleep(0.05)
    pos +=0.7 
    ServoUpDownPos = pos
    if ServoUpDownPos >= 180:
        ServoUpDownPos = 180

#		
def servo_down():
    global ServoUpDownPos
    pos = ServoUpDownPos
    updownservo_appointed_detection(pos)
    #time.sleep(0.05)
    pos -= 0.7
    ServoUpDownPos = pos
    if ServoUpDownPos <= 45:
        ServoUpDownPos = 45
    

#
def servo_left():
    global ServoLeftRightPos
    pos = ServoLeftRightPos
    leftrightservo_appointed_detection(pos)
    #time.sleep(0.10)
    pos += 0.7
    ServoLeftRightPos = pos
    if ServoLeftRightPos >= 180:
        ServoLeftRightPos = 180

#
def servo_right():
    global ServoLeftRightPos
    pos = ServoLeftRightPos
    leftrightservo_appointed_detection(pos)
    #time.sleep(0.10)
    pos -= 0.7 
    ServoLeftRightPos = pos
    if ServoLeftRightPos <= 0:
        ServoLeftRightPos =  0

#
def front_servo_left():
    frontservo_appointed_detection(180)

#
def front_servo_right():
    frontservo_appointed_detection(0)

#
def servo_init():
    servoflag = 0
    servoinitpos = 90
    if servoflag != servoinitpos:        
        frontservo_appointed_detection(servoinitpos)
        updownservo_appointed_detection(servoinitpos)
        leftrightservo_appointed_detection(servoinitpos)
        time.sleep(0.5)
        pwm_FrontServo.ChangeDutyCycle(0)	#
        pwm_LeftRightServo.ChangeDutyCycle(0)	#
        pwm_UpDownServo.ChangeDutyCycle(0)	#

#	
def servo_updown_init():
    updownservo_appointed_detection(90)
	
#
def servo_stop():
    pwm_LeftRightServo.ChangeDutyCycle(0)	#
    pwm_UpDownServo.ChangeDutyCycle(0)	# 
    pwm_FrontServo.ChangeDutyCycle(0)	#

#
def tracking_test():
    global infrared_track_value
    #
    #
    TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
    TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
    TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
    TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
    infrared_track_value_list = ['0','0','0','0']
    infrared_track_value_list[0] = str(1 ^TrackSensorLeftValue1)
    infrared_track_value_list[1] = str(1 ^TrackSensorLeftValue2)
    infrared_track_value_list[2] = str(1 ^TrackSensorRightValue1)
    infrared_track_value_list[3] = str(1 ^TrackSensorRightValue2)
    infrared_track_value = ''.join(infrared_track_value_list)
    

#
def infrared_avoid_test():
    global infrared_avoid_value
    #,,
    #,,
    LeftSensorValue  = GPIO.input(AvoidSensorLeft)
    RightSensorValue = GPIO.input(AvoidSensorRight)
    infrared_avoid_value_list = ['0','0']
    infrared_avoid_value_list[0] = str(1 ^LeftSensorValue)
    infrared_avoid_value_list[1] = str(1 ^RightSensorValue)
    infrared_avoid_value = ''.join(infrared_avoid_value_list)
    	
#
def follow_light_test():
    global LDR_value
    #,,
    #,,
    LdrSersorLeftValue  = GPIO.input(LdrSensorLeft)
    LdrSersorRightValue = GPIO.input(LdrSensorRight)  
    LDR_value_list = ['0','0']
    LDR_value_list[0] = str(LdrSersorLeftValue)
    LDR_value_list[1] = str(LdrSersorRightValue)	
    LDR_value = ''.join(LDR_value_list)
	

#
def tcp_data_postback():
    #
    #
    #      
    global ReturnTemp
    ReturnTemp={}
    distance = Distance_test()
    tracking_test()
    infrared_avoid_test()
    follow_light_test()
    
    ReturnTemp={
        'Distance':distance,
        'Trach_value':infrared_track_value,
        'Avoid_value':infrared_avoid_value,
        'LDR_value':LDR_value
    }
    return ReturnTemp
