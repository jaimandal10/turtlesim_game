#!/usr/bin/env python

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *
from std_msgs.msg import String
import math
import time
import rospy
import random
import sys

global randx,randy,randtheta,collide
global turtle_number
#global base_time = 10

def spawn_random_turtle():

    global turtle_number,randx,randy
    
    rospy.wait_for_service('spawn')
    try:
        turtle_number+=1
        randx = random.randint(2,8)
        randy = random.randint(2,8)
        
        spawn_proxy = rospy.ServiceProxy('spawn',Spawn)
        spawn_proxy(randx,randy,0,'turtle13')
    except rospy.ServiceException:
        print("Error")

def did_turtle_collide(main_turtle_pose):
        global randx,randy
        base_time = 10
        x = main_turtle_pose.x
        y = main_turtle_pose.y
        dist=abs(math.sqrt((x-randx)**2)+(y-randy)**2)
        if(dist<1):  
            print('collided')                   #collision code. spawns new if collide
            rospy.wait_for_service('kill')
            kill_proxy = rospy.ServiceProxy('kill',Kill)
            kill_proxy('turtle13')
            time.sleep(5)
            print('spwaning new')
            spawn_random_turtle()
        else:
            print('not there yet')
            time.sleep(1)
            base_time -= 1
            print(base_time)
        if base_time <= 0:
            print('missed, time reduced')                   #collision code. spawns new if collide
            rospy.wait_for_service('kill')
            kill_proxy = rospy.ServiceProxy('kill',Kill)
            kill_proxy('turtle13')
            #time.sleep(5)
            print('spwaning new')
            spawn_random_turtle()
            base_time = base_time-2 
            if(base_time<=0):
                exit


if __name__ == '__main__':
    turtle_number=1
    rospy.init_node('turtle_colide_checker')
    base_time = 10
    spawn_random_turtle()
    rospy.Subscriber('turtle1/pose',Pose,did_turtle_collide)
    rospy.spin()




