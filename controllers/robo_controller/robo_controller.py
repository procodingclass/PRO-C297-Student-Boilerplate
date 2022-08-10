from controller import Robot
import math
robot = Robot()

timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice("left wheel motor");
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)

right_motor = robot.getDevice("right wheel motor");
right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)

imu= robot.getDevice("inertial unit")
imu.enable(timestep)

ds_front = robot.getDevice("ds_front")
ds_front.enable(timestep)
ds_left = robot.getDevice("ds_left")
ds_left.enable(timestep)
ds_right = robot.getDevice("ds_right")
ds_right.enable(timestep)

movement=0
robo_orientation=180

def move(left_speed,right_speed):
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)       
    
def turn_towards_angle(target_angle,movement):
    if(target_angle != yaw_current):
        move(-1,1) 
    else:
        move(0,0)
        movement+=1    
    return movement 

def move_forward_till_wall_detection(movement):
    if(ds_front_value>300):
        move(15,15)
    else:
        movement+=1
    return movement
    
def find_corner(movement):   
    if(movement==0):
        movement=turn_towards_angle(robo_orientation%360, movement) 
    if(movement==1):
        movement=move_forward_till_wall_detection(movement)
    if(movement==2):
        movement=turn_towards_angle((robo_orientation-90)%360, movement) 
    if(movement==3):
        movement=move_forward_till_wall_detection(movement)     
    if(movement==4):
        movement=turn_towards_angle((robo_orientation-180)%360, movement) 
        
    return movement
    
    
while robot.step(timestep) != -1:
       
    ds_front_value= ds_front.getValue()
    ds_left_value= ds_left.getValue()
    ds_right_value= ds_right.getValue()
    
    angle=imu.getRollPitchYaw()
    
    # the range was -180 to 180 , we change it to 0 to 360
    yaw_current=round(math.degrees(angle[2]))+180
    
    movement = find_corner(movement)