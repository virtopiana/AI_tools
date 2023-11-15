# import required libraries
import cv2
import numpy as np
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import time
import pytesseract
import sys
import string

if len(sys.argv)<2:
    print("Missing filename argument")
    print("Usage: %s <filename>",sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]
# Read input image
vs = FileVideoStream(filename).start()

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        #frame = imutils.resize(frame, width=500)
        if frame is None:
            #Reached end of video file, restart
            vs.stop()
            vs = FileVideoStream(filename).start()
            frame = vs.read()

        # convert input image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # read haarcascade for number plate detection
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

        # Detect license number plates
        plates = cascade.detectMultiScale(gray, 1.2, 5)

        # loop over all plates
        for (x,y,w,h) in plates:
   
            # draw bounding rectangle around the license number plate
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            gray_plates = gray[y:y+h, x:x+w]
            out = pytesseract.image_to_string(gray_plates)
            text = out.replace(" ", "").strip()
            #print("[" + out.strip() + "]")
            if text.isalnum() and len(text) in (6,7):
                print("Plate detected: [" + text.upper() + "]")
            #time.sleep(0.1)
        cv2.imshow("ANPR is Running", frame) 
        key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
        if key == ord("q"):
                break

        # update the FPS counter
        fps.update()


# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()



# save number plate detected
#cv2.imwrite('Numberplate.jpg', gray_plates)
#cv2.imshow('Number Plate', gray_plates)
#cv2.imshow('Number Plate Image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
