#!/usr/bin/python3.8
import sys
import rospy
from rosplan_knowledge_msgs.srv import *
from rosplan_knowledge_msgs.msg import *
from std_srvs.srv import Empty
from rosplan_dispatch_msgs.srv import DispatchService
from diagnostic_msgs.msg import KeyValue

query = []

def call_clear_kb_service():
    print ("Waiting for Clear knowledge Base service")
    rospy.wait_for_service('/rosplan_knowledge_base/clear')
    try:
        print ("Calling Clear knowledge Base Service")
        srv_response  = rospy.ServiceProxy('rosplan_knowledge_base/clear',Empty)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)

def call_problem_generation_service():
    #print ("Waiting for Problem Generation service")
    rospy.wait_for_service('/rosplan_problem_interface/problem_generation_server')
    try:
       # print ("Calling Problem Generation Service")
        srv_response  = rospy.ServiceProxy('/rosplan_problem_interface/problem_generation_server',Empty)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)

def call_planning_service():
    #print ("Waiting for Planning service")
    rospy.wait_for_service('/rosplan_planner_interface/planning_server')
    try:
        print ("Calling Problem Generation Service")
        srv_response  = rospy.ServiceProxy('/rosplan_planner_interface/planning_server',Empty)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)


def call_parse_plan_service():
   # print ("Waiting for Parse Plan service")
    rospy.wait_for_service('/rosplan_parsing_interface/parse_plan')
    try:
        #print ("Calling Parse Plan Service")
        srv_response  = rospy.ServiceProxy('/rosplan_parsing_interface/parse_plan',Empty)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)


def call_dispatch_plan_service():
    print ("Waiting for Dispatch Plan service")
    rospy.wait_for_service('/rosplan_plan_dispatcher/dispatch_plan')
    try:
        print ("Calling Dispatch Plan Service")
        srv_response  = rospy.ServiceProxy('/rosplan_plan_dispatcher/dispatch_plan',DispatchService)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)


def call_update_kb_service():
    print ("Waiting for Update knowledge Base service")
    rospy.wait_for_service('/rosplan_knowledge_base/update')
    try:
        print ("Calling Update knowledge Base Service")
        srv_response  = rospy.ServiceProxy('rosplan_knowledge_base/update',KnowledgeUpdateService)
        srv_response()
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)

old_angle = 0
old_dist = 0

def update_knowledge_base(goal_angle,goal_dist):

    #call_clear_kb_service()
    global old_angle
    global old_dist

    # print("PLANNING DIST" + str(goal_dist))
    # print("PLANNING OLD DIST" + str(old_dist))

    if ((abs(goal_angle) < 7 and old_angle < 7 and abs(goal_dist - old_dist) < 0.3) or  
    ((abs(goal_angle) > 7 and old_angle > 7) and (abs(goal_angle) - old_angle) < 2)):

        print("NOT PLANNING")

    else:
        kus = KnowledgeUpdateServiceRequest()
        kus.knowledge.knowledge_type = 2
        kus.knowledge.attribute_name = 'offset_angle'
        kv = KeyValue()
        kv.key = 'goal_Angle'
        kv.value = 'ga'
        kus.knowledge.function_value = int(abs(goal_angle))
        kus.knowledge.values.append(kv)

        kuc = rospy.ServiceProxy('/rosplan_knowledge_base/update', KnowledgeUpdateService)        
        if not kuc(kus):
            rospy.logerr("KCL: (%s) Robot Goal Angle was not added!" % rospy.get_name())
        call_problem_generation_service()
        call_planning_service()
        # call_parse_plan_service()
        # call_dispatch_plan_service()

    old_angle = abs(goal_angle)   
    old_dist = goal_dist 