'''
                BASHSOFTS (www.bashsofts.com)

         Programmer : Shahab Khalid && Abdul Wakeel

               Below Code Credits To : nemila

    Orignal Code : http://www.forum.coppeliarobotics.com/viewtopic.php?f=11&t=5287

'''
import cv2,numpy,array
from PIL import Image as I


def track_green_object(image):

	# Blur the image to reduce noise
	blur = cv2.GaussianBlur(image, (5,5),0)

	# Convert BGR to HSV
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	# Threshold the HSV image for only green colors
	lower_green = numpy.array([40,70,70])
	upper_green = numpy.array([80,200,200])

	# Threshold the HSV image to get only green colors
	mask = cv2.inRange(hsv, lower_green, upper_green)
	
	# Blur the mask
	bmask = cv2.GaussianBlur(mask, (5,5),0)

	# Take the moments to get the centroid
	moments = cv2.moments(bmask)
	m00 = moments['m00']
	centroid_x, centroid_y = None, None
	if m00 != 0:
		centroid_x = int(moments['m10']/m00)
		centroid_y = int(moments['m01']/m00)

	# Assume no centroid
	ctr = None

	# Use centroid if it exists
	if centroid_x != None and centroid_y != None:
		ctr = (centroid_x, centroid_y)
	return ctr


def ProcessImage(image,resolution):
	image_byte_array = array.array('b', image)
	image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)
	img2 = numpy.asarray(image_buffer)

	# try to find something green
	ret = track_green_object(img2)

	# overlay rectangle marker if something is found by OpenCV
	if ret:
		cv2.rectangle(img2,(ret[0]-15,ret[1]-15), (ret[0]+15,ret[1]+15), (0xff,0xf4,0x0d), 1)

	#f = open("newimagearray.txt","w")
	img3 = cv2.flip(img2,0)
	a = numpy.asarray(img2)
	newArr=[[0,0,0]] * (640*480)
	k = 0
	r,g,b = 0,0,0
	for i in range(0,len(a)):
		for j in range(0,len(a[i])):
			r,g,b = int(a[i][j][0]),int(a[i][j][1]),int(a[i][j][2])
			newArr[k] = [r,g,b]
			#f.write(str(r) + "," + str(g) + "," + str(b) + "\n")
			k+=1
	#f.close()
	return img3,newArr