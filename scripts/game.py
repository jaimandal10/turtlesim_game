#!/usr/bin/env python3

import math
import time
import rospy
import random

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from std_msgs.msg import String

global randx,randy,randtheta,collide
global turtle_number,max_time
global t0

def spawn_random_turtle():

    global turtle_number,randx,randy,t0,score
    
    rospy.wait_for_service('spawn')
    
    try:
        turtle_number+=1
        randx = random.randint(2,8)
        randy = random.randint(2,8)
        
        spawn_proxy = rospy.ServiceProxy('spawn',Spawn)
        spawn_proxy(randx,randy,0,'turtle2')
        t0=time.time()
    except rospy.ServiceException:
        pass

def did_turtle_collide(main_turtle_pose):
        global t0,score,max_time
        t1=time.time()
        if((t1-t0)>max_time):
            rospy.wait_for_service('kill')
            kill_proxy = rospy.ServiceProxy('kill',Kill)
            kill_proxy('turtle1')
            rospy.loginfo("Game over")
            rospy.loginfo("Score:"+"${score}")
            exit()
        
        global randx,randy
        x = main_turtle_pose.x
        y = main_turtle_pose.y
        dist=abs(math.sqrt((x-randx)**2)+(y-randy)**2)
        if(dist<1):
            score+=1
            max_time-=.5
            rospy.wait_for_service('kill')
            kill_proxy = rospy.ServiceProxy('kill',Kill)
            kill_proxy('turtle2')
            time.sleep(5)
            spawn_random_turtle()
    

if __name__ == '__main__':
    turtle_number=1
    score=0
    max_time=10
    rospy.init_node('turtle_colide_checker')
    spawn_random_turtle()
    rospy.Subscriber('turtle1/pose',Pose,did_turtle_collide)
    rospy.spin()