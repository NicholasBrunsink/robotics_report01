#!/usr/bin/env python3

import rospy

from ur5e_control.msg import Plan
from geometry_msgs.msg import Twist

import math

toolpose = Twist()

dataRecieved = False

def twist_callback(data):
	toolpose.linear.x = data.linear.x
	toolpose.linear.x = data.linear.y
	toolpose.linear.z = data.linear.z
	toolpose.angular.x = data.angular.x
	toolpose.angular.y = data.angular.y
	toolpose.angular.z = data.angular.z
	dataRecieved = True

if __name__ == "__main__":
	rospy.init_node('pickup_object', anonymous=True)
	
	plan_pub = rospy.Publisher('/plan', Plan, queue_size = 10)
	toolpose_sub = rospy.Subscriber('/ur5e/toolpose', Twist, twist_callback)

	loop_rate = rospy.Rate(10)
	
	# define a plan variable
	plan = Plan() 
	
	while not dataRecieved:
		pass
	
	plan_point1 = Twist()
	# just a quick solution to send two target points
	# define a point close to the initial position
	plan_point1.linear.x = -0.7
	plan_point1.linear.y = -0.134
	plan_point1.linear.z = 0.43
	plan_point1.angular.x = toolpose.angular.x
	plan_point1.angular.y = toolpose.angular.y
	plan_point1.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point1)
	
	plan_point2 = Twist()
	# define a point away from the initial position
	plan_point2.linear.x = -0.7
	plan_point2.linear.y = -0.134
	plan_point2.linear.z = 0.1
	plan_point2.angular.x = toolpose.angular.x
	plan_point2.angular.y = toolpose.angular.y
	plan_point2.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point2)

	plan_point3 = Twist()
	# just a quick solution to send two target points
	# define a point close to the initial position
	plan_point3.linear.x = -0.134
	plan_point3.linear.y = -0.7
	plan_point3.linear.z = 0.43
	plan_point3.angular.x = toolpose.angular.x
	plan_point3.angular.y = toolpose.angular.y
	plan_point3.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point3)
	
	plan_point4 = Twist()
	# just a quick solution to send two target points
	# define a point close to the initial position
	plan_point4.linear.x = -0.134
	plan_point4.linear.y = -0.7
	plan_point4.linear.z = 0.1
	plan_point4.angular.x = toolpose.angular.x
	plan_point4.angular.y = toolpose.angular.y
	plan_point4.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point4)
	
	while not rospy.is_shutdown():
		# publish the plan
		plan_pub.publish(plan)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
