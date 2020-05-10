import cv2
import time
import numpy as np

## Preparation for writing the ouput video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',fourcc,20.0, (640,480))

##reading from the webcam 
cap = cv2.VideoCapture(0)

## Allow the system to sleep for 3 seconds before the webcam starts
time.sleep(3)

background = 0

## Capture the background in range of 60
for i in range(30):
    ret,background = cap.read()
    if ret == False:
        continue



## Read every frame from the webcam, until the camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    
   
    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Generat masks to detect red color
    lower_red = np.array([155,80,135])
    upper_red = np.array([185,225,255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)


    ## Open and Dilate the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
 
 
    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
 
 
    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
 
 
    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("magic",finalOutput)
    k = cv2.waitKey(10) & 0xff
    if k == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()