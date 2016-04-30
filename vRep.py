'''
                BASHSOFTS (www.bashsofts.com)

         Programmer : Shahab Khalid && Abdul Wakeel

'''
import vrep
import sys
import numpy as np
import cv2
from PIL import Image as I
import array
import Raftaar
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import serial
import os
import threading
import vrep
import sys
import math     
ESCAPE = '\033'
 
window = 0
 
#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1

def InitGL(Width, Height): 
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
 
def keyPressed(*args):
        if args[0] == ESCAPE:
                sys.exit()


def DrawGLScene():
        global X_AXIS,Y_AXIS,Z_AXIS
        global DIRECTION        
        global depthArr
        global rgbArr
        global allVerts,allRGB
        global i,x,y,allEdges
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
        glLoadIdentity()
        glTranslatef(0.0,0.0,-8.0)
        glRotatef(X_AXIS,1.0,0.0,0.0)
        glRotatef(Y_AXIS,0.0,1.0,0.0)
        glRotatef(Z_AXIS,0.0,0.0,1.0)
            
        
        makeScene(allVerts,allRGB)

        glRotatef(90,0.0,1.0,0.0)
        glTranslatef(-.6,0.0,0.0)
        makeScene(allVerts1,allRGB1)


        glTranslatef(+.4,0.0,0.0)
        glRotatef(90,0.0,1.0,0.0)
        glTranslatef(0.0,0.0,-1.0)
        makeScene(allVerts0,allRGB0)


        glTranslatef(0.0,0.0,1.0)
        glRotatef(90,0.0,1.0,0.0)
        glTranslatef(0.0,0.0,-1.0)
        makeScene(allVerts2,allRGB2)
        
        #X_AXIS = X_AXIS - 5.0
        Y_AXIS = Y_AXIS - 5.0
        #Z_AXIS = Z_AXIS - 0.30
        glTranslatef(+.2,0.0,-1.0)
        #Y_AXIS = 45
 
        glutSwapBuffers()



def makeScene(allVerts,allRGB):
        glBegin(GL_POINTS)
        for vert in range(0,len(allVerts)):                                                        
                glColor3f(allRGB[vert][0],allRGB[vert][1],allRGB[vert][2])    
                glVertex3f(allVerts[vert][0],allVerts[vert][1],allVerts[vert][2])  
        glEnd()
def main():
 
        global window
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutInitWindowPosition(200,200)        

        window = glutCreateWindow('OpenGL AND Vrep')

        glutDisplayFunc(DrawGLScene)
        glutIdleFunc(DrawGLScene)
        glutKeyboardFunc(keyPressed)
        InitGL(800, 600)
        glutMainLoop()



def applyDepth_RGB(depthArr,rgbArr):
        myVerts = [j for j in range(0,len(depthArr)) if j % 12 == 0]
        perRow = len(myVerts) / 480
        k = 0
        allVerts = [[-1.0,-1.0,-1.0]] * len(myVerts)
        allRGB = [[-1.0,-1.0,-1.0]] * len(myVerts)
        for i in myVerts:
                if depthArr[i] != 1 and depthArr[i] > 0.15: #skipping far and near points
                        #print "i = " + str(i) + "color = " + str(rgbArr[i][0]) + "," + str(rgbArr[i][1]) + "," + str(rgbArr[i][2]) + "\n"                        
                        #glColor3f(float(rgbArr[i][0]) / 255.0,float(rgbArr[i][1]) / 255.0,float(rgbArr[i][2]) / 255.0)                        
                        x = float(i % 640)                        
                        y = math.floor(float(i / 640))

                        x = float(x / 640.0) * 4 - 2
                        y = float(y / 480.0) * 4 - 3



                        #glVertex3f( x,y,depthArr[i])
                        allVerts[k] = [x,y,depthArr[i]]
                        allRGB[k] = [float(rgbArr[i][0]) / 255.0,float(rgbArr[i][1]) / 255.0,float(rgbArr[i][2]) / 255.0]
                        k+=1

                                     
        return allVerts,allRGB



def fetchKinect(depthSTR,rgbSTR):
        errorCodeKinectRGB,kinectRGB=vrep.simxGetObjectHandle(clientID,rgbSTR,vrep.simx_opmode_oneshot_wait)
        errorCodeKinectDepth,kinectDepth=vrep.simxGetObjectHandle(clientID,depthSTR,vrep.simx_opmode_oneshot_wait)

        
        errorHere,resolution,image=vrep.simxGetVisionSensorImage(clientID,kinectRGB,0,vrep.simx_opmode_oneshot_wait)
        img,imgArr=Raftaar.ProcessImage(image,resolution)        
        rgbArr=np.array(imgArr)

        errorHere,resol,depth=vrep.simxGetVisionSensorDepthBuffer(clientID,kinectDepth,vrep.simx_opmode_oneshot_wait)
        depthArr=np.array(depth)


        return depthArr,rgbArr


def processScene():
        global allVerts,allRGB,depthArr,rgbArr,allEdges
        global allVerts0,allRGB0,depthArr0,rgbArr0,allVerts1,allRGB1,allVerts2,allRGB2

        allVerts,allRGB = applyDepth_RGB(depthArr,rgbArr)
        allVerts0,allRGB0 = applyDepth_RGB(depthArr0,rgbArr0)
        allVerts1,allRGB1 = applyDepth_RGB(depthArr1,rgbArr1)
        allVerts2,allRGB2 = applyDepth_RGB(depthArr2,rgbArr2)
        
if __name__ == "__main__":

        global depthArr,depthArr0,depthArr1
        global rgbArr,rgbArr0,rgbArr1
        #Connection
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19998,True,True,5000,5)

        if clientID != -1:
                print "Connected to remote API Server"
                
        else:
                print "Connection not succesfull"
                sys.exit("Could not connect")


        depthArr,rgbArr = fetchKinect('kinect_depth','kinect_rgb')
        depthArr0,rgbArr0 = fetchKinect('kinect_depth#0','kinect_rgb#0')
        depthArr1,rgbArr1 = fetchKinect('kinect_depth#1','kinect_rgb#1')
        depthArr2,rgbArr2 = fetchKinect('kinect_depth#2','kinect_rgb#2')

        processScene()
        main()

