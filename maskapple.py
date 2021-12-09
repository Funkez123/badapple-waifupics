import cv2
import numpy as np
import glob, random

video = "video.mp4" # Bad-Apple videofile
video_output_res = (1920,1080)
dimension = (64,36) # Pixelmap-dimension
whiteframe_nr = 86 # NR of pictures that make up the "background"

cap = cv2.VideoCapture(video)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
size = (width, height)

background_white = np.zeros((video_output_res[1],video_output_res[0],3), np.uint8)
background_black = np.zeros((video_output_res[1],video_output_res[0],3), np.uint8)
mosaic_pixel = (int(video_output_res[1]/dimension[1]),int(video_output_res[0]/dimension[0]))

## White pixel

progress_max = dimension[0]*dimension[1]
progress_counter = 0

y = 0
x = 0
for y in range(dimension[1]):
    for x in range(dimension[0]):
        progress_counter = progress_counter + 1
        if progress_counter < progress_max:
            print("Preprocessing... " + str(int((progress_counter/progress_max)*100))+"%")

        frame = cv2.imread("frame"+str(random.randint(0,whiteframe_nr-1))+".jpg")
        frame = cv2.resize(frame, mosaic_pixel, interpolation = cv2.INTER_AREA)
        background_white[y*mosaic_pixel[0]:y*mosaic_pixel[0]+frame.shape[0], x*mosaic_pixel[0]:x*mosaic_pixel[0]+frame.shape[1]] = frame


background_white = cv2.resize(background_white, video_output_res, interpolation = cv2.INTER_AREA)

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error reading the video file")
count = 0

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    frame = cv2.resize(frame, dimension, interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    weird_returnvalue, bwframe = cv2.threshold(gray, 123, 255,cv2.THRESH_BINARY)
    output_frame = cv2.resize(bwframe, video_output_res, interpolation = cv2.INTER_AREA)
    masked1 = cv2.bitwise_and(background_white, background_white, mask=output_frame)
    cv2.imshow("output",masked1)
    count = count + 1

    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else:
    break

cap.release()
cv2.destroyAllWindows()
