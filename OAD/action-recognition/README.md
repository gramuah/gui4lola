# SVC for Unsupervised Temporal Action Proposals

Online Action Detection (OAD) with C3D. The C3D model is trained on the UCF101 dataset (Thumos14 is a subset of UCF101). The model achieves about a 73% clip accuracy on the first test split. (Kind of a good number).
The application is limited to only the categories that we want, though it is trained to detect the 101 categories.

### Before running

 This application was prepared for Python 3.8 and pytorch 1.4, which is ready to use with cudatoolkit=10.0 (installed in Atenea). The dependencies are:
 - opencv=4.4.0
 - numpy=1.19.1

My recommendation is to use conda (it is what I used), but if it's not possible, a virtual environment should work. If conda works, the same environment can be built with the following file:
 - source/c3d-env.yml

### Usage

To run the OAD application:

1) Go to source/ directory
2) Run the command: python action_recognition.py

### Something about the files:

 - source/c3d_model.py: This file contains the pytorch implementation of the C3D model.
 - source/clip_classification.py: It's a python class that loads the C3D model with its weights and has a function to predict the action category given a 16-frame clip.
 - source/action_recognition.py: It's the main file of the OAD application. Everything happens inside a loop that is active as long as the camera is collecting frames.
