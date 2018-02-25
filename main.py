import map
import operator

# image processing imports
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, img = cap.read()

cv2.namedWindow("raw")
cv2.namedWindow("avg")

# base value to compare new readings to
background = (0,0,0)	

# threshold value for occupancy
thresh = 5

while ret:
	ret, img = cap.read()
	cv2.imshow("raw", img)

	# calculate and display average color across image
	avg = img
	average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]	
	avg[:]  = average_color
	cv2.imshow("avg", img)

	change = np.subtract(background, average_color)
	percent_change = abs(sum(change)/len(change)/255*100)
	
	state = "Unoccupied"
	if (percent_change > thresh):
		state = "Occupied"

	print "Percent Change: {:.2f}%		State: {}".format(percent_change, state)
	
	# check user input
	# b: update background
	# q: quit		
	key = cv2.waitKey(1)
	if key & 0xFF == ord('b'):
		background = average_color
	elif key & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

