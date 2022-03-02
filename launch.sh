#!/bin/bash

{ roslaunch lola2_global basic_lola.launch && \
roslaunch logitech_f710_joy_ros joy_teleop.launch && \
python3 ~/gui4lola/main.py ;}