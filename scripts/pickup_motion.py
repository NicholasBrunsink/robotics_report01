#!/usr/bin/env python3

# importing dependancies
import rospy
from ur5e_control.msg import Plan
from geometry_msgs.msg import Twist
import math

# initializing Twist to store initial tool pose
toolpose = Twist()
# initializing flag for determining when toolpose data is recieved
dataRecieved = False

def twist_callback(data):
	'''
	called when /ur5e/toolpose is published to store initial toolpose data
	'''
	global dataRecieved
	if not dataRecieved:
		toolpose.linear.x = data.linear.x
		toolpose.linear.x = data.linear.y
		toolpose.linear.z = data.linear.z
		toolpose.angular.x = data.angular.x
		toolpose.angular.y = data.angular.y
		toolpose.angular.z = data.angular.z
		dataRecieved = True
	print("Initial Position:\n",data)
	

def main():
	# initialize node
	rospy.init_node('pickup_object', anonymous=True)
	
	# create publisher to publish Plan 
	plan_pub = rospy.Publisher('/plan', Plan, queue_size = 10)
	# create subscriber to grab initial position and rotation
	toolpose_sub = rospy.Subscriber('/ur5e/toolpose', Twist, twist_callback)

	# hold execution until initial position and rotation is set
	global dataRecieved
	while not dataRecieved:
		pass
	# unsubscribe from /ur5e/toolpose after initial pos is stored
	toolpose_sub.unregister()
	
	# set loop rate to 10 Hz
	loop_rate = rospy.Rate(10)
	
	# define a plan variable
	plan = Plan() 
	
	plan_point1 = Twist()
	# define a point at the initial position
	plan_point1.linear.x = -0.7
	plan_point1.linear.y = -0.133
	plan_point1.linear.z = 0.43
	plan_point1.angular.x = toolpose.angular.x
	plan_point1.angular.y = toolpose.angular.y
	plan_point1.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point1)
	
	plan_point2 = Twist()
	# define a point  below initial position
	plan_point2.linear.x = -0.7
	plan_point2.linear.y = -0.133
	plan_point2.linear.z = 0.1
	plan_point2.angular.x = toolpose.angular.x
	plan_point2.angular.y = toolpose.angular.y
	plan_point2.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point2)

	plan_point3 = Twist()
	# Define a point above the final position
	plan_point3.linear.x = -0.134
	plan_point3.linear.y = -0.7
	plan_point3.linear.z = 0.43
	plan_point3.angular.x = toolpose.angular.x
	plan_point3.angular.y = toolpose.angular.y
	plan_point3.angular.z = toolpose.angular.z
	# add this point to the plan
	plan.points.append(plan_point3)
	
	plan_point4 = Twist()
	# define point away from initial position to be the final point
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
main()
