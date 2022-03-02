#!/bin/bash

(python3 ~/gui4lola/main.py & \
roslaunch logitech_f710_joy_ros joy_teleop.launch & \
roslaunch lola2_global basic_lola.launch)