# Multi-Application Implementation Using Path Planning and Computer Vision
This repository uses computer vision and SLAM to enable an Ohmni telepresence robot to follow a person in its filed of view automatically.

## Getting started
This repository contains different ROS packages. You need to have ros-noetic installed on your machine. 
The workspace was deployed to automate an Ohmni Telepresence Developer Robot.

### Prerequisite
sudo apt-get install ros-noetic-tf2-sensor-msgs
sudo apt install flex bison freeglut3-dev libbdd-dev python-catkin-tools ros-$ROS_DISTRO-tf2-bullet

## Build
1. Create a catkin Workspace
2. Go to your catkin workspace and pull git pull src folder to the workspace 
3. Build your catkin workspace using catkin_make.

## Citation

Please cite this paper in your publications if the module helps your research.

@InProceedings{10.1007/978-3-031-43360-3_13,
author="Aboki, Nasiru
and Georgievski, Ilche
and Aiello, Marco",
editor="Iida, Fumiya
and Maiolino, Perla
and Abdulali, Arsen
and Wang, Mingfeng",
title="Automating a Telepresence Robot for Human Detection, Tracking, and Following",
booktitle="Towards Autonomous Robotic Systems",
year="2023",
publisher="Springer Nature Switzerland",
address="Cham",
pages="150--161",
abstract="The operation of a telepresence robot as a service robot has gained wide attention in robotics. The recent COVID-19 pandemic has boosted its use for medical uses, allowing patients to interact while avoiding the risk of contagion. While telepresence robots are designed to have a human operator that controls them, their sensing and actuation abilities can be used to achieve higher levels of autonomy. One desirable ability, which takes advantage of the mobility of a telepresence robot, is to recognize people and the space in which they operate. With the ultimate objective to assist individuals in office spaces, we propose an approach for rendering a telepresence robot autonomous with real-time, indoor human detection and pose classification, with consequent chaperoning of the human. We validate the approach through a series of experiments involving an Ohmni Telepresence Robot, using a standard camera for vision and an additional Lidar sensor. The evaluation of the robot's performance and comparison with the state of the art shows promise of the feasibility of using such robots as office assistants.",
isbn="978-3-031-43360-3"
}


###Link to the paper

https://link.springer.com/chapter/10.1007/978-3-031-43360-3_13
