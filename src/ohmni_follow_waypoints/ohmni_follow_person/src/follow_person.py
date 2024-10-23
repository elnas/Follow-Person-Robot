#!/usr/bin/python3.8
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, fabs

goal_dist = 0.0
goal_angle = 0

 
def stop_robot():
    while speed.linear.x == 0:
        speed.linear.x = speed.linear.x - 0.06
        print ("Stop Robot " + str(speed.linear.x))

def person_callback(msg):

    global goal_angle
    global goal_dist

    goal_angle = msg.y
    goal_dist = msg.z

    orient_robot()

def orient_robot():
    global goal_angle
    global goal_dist

    print ("angle_to_goal " + str(goal_angle))
    
    angular_vel = 0.1#abs(goal_y/158)
    ## Align the robot to goal position
    if  goal_angle > 7:
        #speed.linear.x = 0.0
        #stop_robot()
        speed.angular.z = (goal_angle/128)
        print ("Rotate Clockwise " + str(speed.angular.z))  

    
    elif goal_angle < -7 :
        #speed.linear.x = 0.0
        #stop_robot()
        speed.angular.z = (goal_angle/128) 
        print ("Rotate Anti-Clockwise " + str(speed.angular.z))  

    else:
        speed.angular.z = 0.0
        ## Robot is aligned. Now go straight.
        if (goal_dist > 1 and goal_dist < 6):
            print("Goal Dist " + str(goal_dist))
            speed.linear.x = (goal_dist / 11)

            if (speed.linear.x > 0.4):
                speed.linear.x = 0.4
            print ("Go Straight " + str(speed.linear.x))  
   
        elif (goal_dist < 0.6):
            print ("Go backward")
            speed.linear.x = -0.15

        else:
            if (speed.linear.x <=0):
                speed.linear.x = 0.0
                
            else:
                speed.linear.x = speed.linear.x - 0.04
            print ("Stop Robot " + str(speed.linear.x))

            
    pub.publish(speed)
 

rospy.init_node("follow_person")
pub = rospy.Publisher("/tb_cmd_vel", Twist, queue_size = 1)
sub = rospy.Subscriber("/person/points", Point, person_callback)

speed = Twist()
rate = rospy.Rate(1)

while not rospy.is_shutdown():
     rate.sleep()

