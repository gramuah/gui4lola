#!/bin/bash

roslaunch lola2_global basic_lola.launch &
roslaunch logitech_f710_joy_ros joy_teleop.launch &
cd ~/gui4lola/ || exit
python3 main.py
