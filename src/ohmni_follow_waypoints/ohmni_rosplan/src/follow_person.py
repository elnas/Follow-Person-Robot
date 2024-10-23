#!/usr/bin/python3.8

from array import array
from audioop import avg
import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from darknet_ros_msgs.msg import BoundingBoxes
from sensor_msgs.msg import LaserScan
import math
import tf
import numpy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from std_msgs.msg import String
from rosplan_dispatch_msgs.msg import CompletePlan
from ohmni_problem_gen import update_knowledge_base


#Global variable to read camera data
Image_data = 0
speed = Twist()
person_avg_distance = 0
offset_angle = 0
plan = ""
plan_recieved = False
plan_goal_distance = 0
plan_goal_angle = 0

def raw_image_callback(data):

    global person
    br = CvBridge()

    rospy.logdebug("Recieving video frames")

    img = br.imgmsg_to_cv2(data, "rgb8")
    dim2 = (data.width,data.height)

    #print("Raw image dimension " + str(dim2))

    #width = int(data.width * 0.80)
    #height = int(data.height * 0.80)
    #dim = (width, height)

    #mg_resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    #try:
        #cv2.rectangle(img,(person.xmin,person.ymin),(person.xmax,person.ymax),(0,255,0),2)
        #cv2.imshow('Camera', img)
        #cv2.waitKey(1)

    #except:    
        #print("")
    

process_count = 0
def boundingbox_callback(data):
    global camera_angle
    global person
    global process_count
    #print("data size " + str(len(data.bounding_boxes)))
    for object in data.bounding_boxes:
        if object.probability > 0.85:
            
            process_count = process_count + 1
            if process_count%2 == 0 :
                person = object
                centre_x = person.xmin + (person.xmax - person.xmin )/2
                centre_y = person.ymin + (person.ymax - person.ymin)/2

                #print(person)
                #print("centre_x " + str(centre_x))
                #print("centre_y " + str(centre_y))
                
                camera_angle = get_camera_angle(centre_x)
                offset_angle = get_offset_angle(camera_angle)
                publish_data()

                plan_goal_angle = offset_angle
                plan_goal_distance = person_avg_distance
                update_knowledge_base(plan_goal_angle, plan_goal_distance)


def plan_callback(msg):
    global plan, plan_recieved
    plan = msg.data
    plan_recieved = True

    global offset_angle
    global person_avg_distance

    print("Plan Received: " + str(plan))

    if 'move' in plan:
        move_robot(offset_angle,person_avg_distance)
        print('Plan : move robot')
    elif 'orientation' in plan:
        orient_robot(offset_angle,person_avg_distance)
        print('Plan: orient robot')
    else:
        print("Plan: Wrong Action ?? ")

def move_robot(goal_angle,goal_dist):
    speed.angular.z = 0.0
    ## Robot is aligned. Now go straight.
    if (goal_dist > 1 and goal_dist < 6):
        print("Goal Dist " + str(goal_dist))
        speed.linear.x = (goal_dist / 11)
        if speed.linear.x > 0.4:
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
    

def orient_robot(goal_angle,goal_dist):

    print ("angle_to_goal " + str(goal_angle))
    
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

    pub.publish(speed)

def get_camera_angle(centre_x):
    camera_angle = (centre_x * 140 ) / 640
    #print("camera_angle " + str(camera_angle))
    return camera_angle

def get_offset_angle(camera_angle):
    global offset_angle
    offset_angle = 70 - camera_angle
    return offset_angle

def publish_data():
    global person_avg_distance
    goal_point = Point()
    goal_point.x = 0
    goal_point.y = offset_angle
    goal_point.z = person_avg_distance ## Not a Z co-ordinate instead Send distance from polar co-ordinates
    #pub_person_points.publish(goal_point)

    #print(str(goal_point))


def scan_callback(laserMsg):
    global person_avg_distance
    array = np.array(laserMsg.ranges[355:365])
    #print("Averaging array : " + str(array))
    person_avg_distance = array[array!=0].mean() 
    #print("Averaging Distance  : " + str(person_avg_distance))

if __name__ == '__main__':    
    
    try:        
        rospy.init_node('identifyperson', disable_signals= True)
        camera_sub = rospy.Subscriber('/main_cam/image_raw', Image, raw_image_callback)
        bound_sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, boundingbox_callback)
        scan_sub = rospy.Subscriber('/scan', LaserScan, scan_callback)
        sub_planner_op = rospy.Subscriber("/rosplan_planner_interface/ohmni_planner_output", String, plan_callback)

        pub = rospy.Publisher("/tb_cmd_vel", Twist, queue_size = 1)
        

        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            rate.sleep()
            # for i in range(14):
            #     offset_angle = i
            #     person_avg_distance = i
            #     publish_data()
            #     update_knowledge_base(offset_angle)

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
