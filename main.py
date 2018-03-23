#!/usr/bin/python3

import map
import operator

# image processing imports
import cv2
import numpy as np


'''
@requires None
@modifies None
@returns List of VideoCapture objects
detect all video capture devices currently connected
returns list of camera objects
'''
def detect_cameras():
	num_cameras = 0
	cameras = []
	while True:
		print("Checking device {}...".format(num_cameras))
		capture = cv2.VideoCapture(num_cameras)
		success, frame = capture.read()
		if success == True:
			print("Success!")
			cameras.append(capture)
			num_cameras += 1
		else:
			print("Detected {} devices.".format(num_cameras))
			return cameras

'''
@requires number of connected cameras
@modifies None
@returns None
spawns two windows per connected camera to show raw/processed footage
accepts the number of connected cameras as argument
'''
def setup_windows(num_cameras):
	for camera_num in range(0, num_cameras):
		cv2.namedWindow("camera {} raw".format(camera_num))
		cv2.namedWindow("camera {} avg".format(camera_num))

'''
@requires List of connected cameras
@modifies None
@returns None
main loop to read camera data and detect occupancy
accepts list of VideoCapture objects as argument
'''
def detect_occupancy(cameras):
	num_cameras = len(cameras)
	background = (0,0,0) # base value to compare new readings to
	threshold = 5 # threshold percent for occupancy

	while True:
		for camera_num in range(0, num_cameras):
			success, frame = cameras[camera_num].read()
			if not success:
				return

			cv2.imshow("cam{} raw".format(camera_num), frame)

			# calculate and display average color across image
			averaged_frame = frame
			average_color = [frame[:, :, i].mean() for i in range(frame.shape[-1])]	
			averaged_frame[:]  = average_color
			cv2.imshow("cam{} avg".format(camera_num), frame)

			change = np.subtract(background, average_color)
			percent_change = abs(sum(change)/len(change)/255*100)
			
			state = "Unoccupied"
			if (percent_change > threshold):
				state = "Occupied"

			print ("CAM{}        Percent Change: {:.2f}%    State: {}".format(camera_num, percent_change, state))
		
		# check user input
		# b: update background
		# q: quit		
		key = cv2.waitKey(1)
		if key & 0xFF == ord('b'):
			background = average_color
		elif key & 0xFF == ord('q'):
			break

'''
@requires List of connected cameras
@modifies None
@returns None
frees VideoCapture objects and closes windows to ensure exit goes smoothly
accepts a list of VideoCapture objects as argument
'''
def free(cameras):
	# free resources
	for camera in cameras:
		camera.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	cameras = detect_cameras()
	setup_windows(len(cameras))
	detect_occupancy(cameras)
	free(cameras)
