This repository contains our work on Vrep (Robotic Simulation Software) and Python. The "Raftaar.py" get the virtual kinect RGB from Vrep and "vRep.py" does the actual modeling process in python. "vRep.py" takes the kinect depth from Vrep and RGB from "Raftaar.py" and models the scene on a python interface.

Requirements:
1. VRep python API
2. Python 2.7
3. VRep simulation software
4. OpenGL python liberaries (GL, GLUT, GLU)

How to:
1. Download Vrep from (www.coppeliarobotics.com) and install
2. Go to vrep/programming/remoteApiBindings/python and copy all the files to your working directory
3. Run Vrep and load the scene
4.Execute the python script in the terminal
