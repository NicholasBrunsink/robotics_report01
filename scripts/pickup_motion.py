#!/usr/bin/env python3

import rospy

from ur5e_control.msg import Plan
from geometry_msgs.msg import Twist

import math

plan_msg = Plan()

if __name__ == "__main__":
	rospy.init_node('pickup_object', anonymous=True)
	
	plan_pub = rospy.Publisher('/plan', Plan, queue_size = 10) 

	loop_rate = rospy.Rate(10)
	
	# define a plan variable
	plan = Plan()
	
	plan_point1 = Twist()
	# just a quick solution to send two target points
	# define a point close to the initial position
	plan_point1.linear.x = 0.0
	plan_point1.linear.y = -0.2
	plan_point1.linear.z = 0.5
	plan_point1.angular.x = 1.57
	plan_point1.angular.y = 0.0
	plan_point1.angular.z = 0.0
	# add this point to the plan
	plan.points.append(plan_point1)
	
	plan_point2 = Twist()
	# define a point away from the initial position
	plan_point2.linear.x = -0.2
	plan_point2.linear.y = 0.0
	plan_point2.linear.z = 0.5
	plan_point2.angular.x = 0.0
	plan_point2.angular.y = 0.0
	plan_point2.angular.z = 0.0
	# add this point to the plan
	plan.points.append(plan_point2)

	
	
	while not rospy.is_shutdown():
		# publish the plan
		plan_pub.publish(plan)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
