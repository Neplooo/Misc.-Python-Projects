import math
import cv2
import numpy as np
import matplotlib as mpl
import scipy.interpolate

#-----Constants-----#

RED_SAMP_LOW = np.array([0, 50, 50])
RED_SAMP_HIGH = np.array([5, 255, 255])




#-----Input Formatting-----#

#Get img data
sample = cv2.imread("src/Screenshot 2025-03-20 200348.png", cv2.IMREAD_COLOR)

#Scale it so that it actually fits on my screen
scaleFactor = 150
imgWidth = int(sample.shape[1] * scaleFactor / 100)
imgHeight = int(sample.shape[0] * scaleFactor / 100)
dim = (imgWidth, imgHeight)
scaledSample = cv2.resize(sample, dim)



#-----Create Bounding Boxes Around Samples-----#

#Get HSV value so that we can analyze the image
sampleHSV = cv2.cvtColor(scaledSample, cv2.COLOR_BGR2HSV)

#Make a color mask to get the red samples
redColorMask = cv2.inRange(sampleHSV, RED_SAMP_LOW, RED_SAMP_HIGH)

#Dilate the color mask to get better mask results
kernel = np.ones((3,3), np.uint8)
dilatedSample = cv2.dilate(redColorMask, kernel, iterations=5)

#Fit contours around the samples
sampleContours = cv2.findContours(dilatedSample, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

thresholdArea = 30000
filteredContours = []

#Find largest contours
for cnt in sampleContours[0]:
    if cv2.contourArea(cnt) >= thresholdArea:
        filteredContours.append(cnt)

#Create a list of all of the bounding boxes
rects = []

#Fill the list with all of the samples
for cnt in filteredContours:
    #Fit a bounding rectangle around the contour
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int64(box)
    rects.append(box)

#Debuggin it rn
print(rects)

#Draw the bounding boxes for coolness effects
boundedSample = cv2.drawContours(scaledSample, rects, -1, (0, 255, 0), 2)






#-----Find Middle of Sample-----#

#First, we need the centroids for all of the boxes
boxCenters = np.empty([len(rects), 2])

#Create a counter because GG
listIterator = 0

#Loop through every rectangle
for rect in rects:

    #Create two temporary arrays for the x and y values we will capture
    xPoints = np.empty([2])
    yPoints = np.empty([2])
    for point in range(0, 2):
        xPoints[point] = rect[point*2, 0] #Capture the values
        yPoints[point] = rect[point*2, 1]

    #print(xPoints)
    #print(yPoints)

    #Get the values and append them to the data arrays
    midX = (xPoints[0] + xPoints[1]) / 2
    midY = (yPoints[0] + yPoints[1]) / 2
    boxCenters[listIterator] = [midX, midY] #Add the data to the boxcenters variable

    #Update the counter
    listIterator += 1

#Format the center points so that OpenCV does not poop itself
boxCenters = np.int64(boxCenters)



#-----Find Closest Sample to Center-----#

#Create arrays for the midpoint and one for the closest sample
midpoint = np.array([imgWidth/2, imgHeight/2])
closestSample = np.array([boxCenters[0][0], boxCenters[0][1], 0])

#Create a counter to keep track of indeces
centerCounter = 0;

#Loop through every bounding box center point
for center in boxCenters:

    isCloserThanClosest = center[0] > closestSample[0] and center[1] > closestSample[1]
    isLessThanMidpoint = center[0] <= midpoint[0] and center[1] <= midpoint[1]

    #If the center is closer to the midpoint, make that the new closest sample
    if isCloserThanClosest and isLessThanMidpoint:
        closestSample[0] = center[0]
        closestSample[1] = center[1]
        closestSample[2] = centerCounter #IMPORTANT: This is the index of the closest sample in the array

    #Update the counter
    centerCounter += 1

#print(closestSample)




#-----Find Angle Of sample relative to Cam-----#

CENTER_LINE_SLOPE = 10000000000
CLOSEST_BOX_INDEX = closestSample[2]
#AROC = Change in X / Change in Y

try:
    CLOSEST_BOX_SLOPE =  (rects[CLOSEST_BOX_INDEX][0][1] - rects[CLOSEST_BOX_INDEX][1][1]) / (rects[CLOSEST_BOX_INDEX][0][0] - rects[CLOSEST_BOX_INDEX][1][0])
except ZeroDivisionError:
    closestBoxTheta = 90

#Formula of Angle Between two lines:
# tan(Theta) = m1 - m2 / 1 + m1*m2
# Get theta with Arc Tangent

if math.isinf(CLOSEST_BOX_SLOPE):
    closestBoxTheta = 0
else:
    closestBoxTheta = math.atan(abs((CLOSEST_BOX_SLOPE - CENTER_LINE_SLOPE) / (1 + CLOSEST_BOX_SLOPE*CENTER_LINE_SLOPE)))

closestBoxTheta = math.degrees(closestBoxTheta)

print(closestBoxTheta)


degToServoPos = scipy.interpolate.interp1d([0, 360], (0.0, 1.0))

servoPos = round(float(degToServoPos(closestBoxTheta)), 2)



#-----Format Findings-----#

#Map out all of the center points nicely
for center in boxCenters:
    cv2.putText(boundedSample, "X: " + str(center[0]) + ", Y: " + str(center[1]), ((center[0]) + 10, center[1]), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.circle(boundedSample, (center[0], center[1]), 1, (0, 255, 0), 2)

cv2.putText(boundedSample, "Servo Position to Align: " + str(servoPos), ((boxCenters[0][0]) + 10, boxCenters[0][1] + 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)

cv2.imshow("Sample", boundedSample)



#-----End Program-----#

cv2.waitKey(0)

cv2.destroyAllWindows()