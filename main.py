#!/usr/bin/python3

import map
import operator

# image processing imports
import cv2
import numpy as np

# detect all video capture devices currently connected
# returns list of camera objects
def detect_cameras():
	num_cams = 0
	caps = []
	while True:
		print("Checking device {}...".format(num_cams))
		cap = cv2.VideoCapture(num_cams)
		ret, _ = cap.read()
		print(ret)
		if ret == True:
			print("Success!")
			caps.append(cap)
			num_cams += 1
		else:
			print("Detected {} devices.".format(num_cams))
			return caps

# spawns two windows per connected camera to show raw/processed footage
# accepts the number of connected cameras as argument
def setup_windows(num_cams):
	for cam_num in range(0, num_cams):
		cv2.namedWindow("cam{} raw".format(cam_num))
		cv2.namedWindow("cam{} avg".format(cam_num))

# main loop to read camera data and detect occupancy
# accepts list of VideoCapture objects as argument
def detect_occupancy(caps):
	num_cams = len(caps)
	background = (0,0,0) # base value to compare new readings to
	thresh = 5 # threshold percent for occupancy

	while True:
		for cam_num in range(0, num_cams):
			ret, img = caps[cam_num].read()
			if not ret:
				return

			cv2.imshow("cam{} raw".format(cam_num), img)

			# calculate and display average color across image
			avg = img
			average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]	
			avg[:]  = average_color
			cv2.imshow("cam{} avg".format(cam_num), img)

			change = np.subtract(background, average_color)
			percent_change = abs(sum(change)/len(change)/255*100)
			
			state = "Unoccupied"
			if (percent_change > thresh):
				state = "Occupied"

			print ("CAM{}        Percent Change: {:.2f}%    State: {}".format(cam_num, percent_change, state))
		
		# check user input
		# b: update background
		# q: quit		
		key = cv2.waitKey(1)
		if key & 0xFF == ord('b'):
			background = average_color
		elif key & 0xFF == ord('q'):
			break

# frees VideoCapture objects and closes windows to ensure exit goes smoothly
# accepts a list of VideoCapture objects as argument
def free(caps):
	# free resources
	for cap in caps:
		cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	caps = detect_cameras()
	setup_windows(len(caps))
	detect_occupancy(caps)
	free(caps)
