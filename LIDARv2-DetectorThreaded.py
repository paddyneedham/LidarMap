#Test for GPIO
from rplidar import RPLidar
import Jetson.GPIO as GPIO
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import cv2
import threading
import i2c

exitFlag = 0

#setup lidar device
lidar = RPLidar('/dev/ttyUSB0')

#Setup output pin to turn motor on
output_pin = 15


DMAX = 80000
IMIN = 50
IMAX = 500

x_DIMENSION = 5000
Y_DIMENSION = 5000

img = np.zeros((1000, 1000, 1))


class Thread1 (threading.Thread): 
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
	def run(self):
		print ('starting thread')
		run_lidar()
		print ('stopping')

class ThreadWatchDog (threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
	def run(self):
		while True:
			i2c.SendHeartBeat()
			print ('send hb')
			time.sleep(1)

def main():

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(output_pin, GPIO.OUT, initial = GPIO.HIGH)	
	
	#cv2.imshow('test', img)
	#cv2.waitKey()
	#time.sleep(20)	

	thread2 = ThreadWatchDog(1)
	thread2.start()

	try:
		#img = np.zeros((800, 800))
		start_lidar()
		i2c.LidarOn()
		#wait for started
		time.sleep(1)
		lidar.connect()	

		health = lidar.get_health()
		print(health)
		iterator = lidar.iter_scans()
		
		thread1 = Thread1(1)
		thread1.start()

		while True:
			#run_lidar()
			#detector(img)
			cv2.imshow("test", img)
			cv2.waitKey(1)
			


	finally:
		stop_lidar()
	



def update(num, iterator, line):
	print ('nextscan')
	#scan = next(iterator)
	scan = iterator
	print (scan)
	#time.sleep(1)
	polorcoords = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
	cartesiancoords = np.array([(meas[2]*np.sin(np.radians(meas[1])), meas[2]*np.cos(np.radians(meas[1])))for meas in scan])
	
	line.set_offsets(cartesiancoords)
	intens = np.array([meas[0] for meas in scan])
	line.set_array(intens)
	return line,


def detector(img):
	frame = cv2.convertScaleAbs(img)
	#ret, threash = cv2.threshold(frame, 127, 255, 0)
	frame ,contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	areas = []

	for i in range(0, len(contours)):
		areas.append(cv2.contourArea(contours[i]))
		mass_centres_x = []
		mass_centres_y = []

	for i in range(0, len(contours)):
		#M = cv2.moments(contours[i], 0)
		#mass_centres_x.append(int(M['m10']/M['m00']))
		#mass_centres_y.append(int(M['m01']/M['m00']))
		print ('Num particles: ', len(contours))

	for i in range(0, len(contours)):
		print ('Area', (i + 1), ':', areas[i])

	cv2.drawContours(img, contours, -1 (0,255,0), 3)

	#for i in range(0, len(contours)):
	#	print 'Centre',(i + 1),':', mass_centres_x[i], mass_centres_y[i]    

def run_lidar():
	
	try:

		for scan in lidar.iter_scans():
			if len(scan) > 100:
				for (_, angle, distance) in scan:
					radians = np.radians(angle)
					x = int((((distance * np.cos(radians))/10) + 500))
					y = int((((distance * np.sin(radians))/10) + 500))
					img[x,y] = 1

	
	finally:
		print('stopping')
	

def start_lidar():
	GPIO.output(output_pin, GPIO.LOW)


def stop_lidar():
	GPIO.output(output_pin, GPIO.HIGH)
	GPIO.cleanup()
	return

if __name__ == '__main__':
	main()



