import time

import cv2
import numpy

fourcc = cv2.VideoWriter_fourcc(*'XVID')

output_file = cv2.VideoWriter('invis_cloak.avi', fourcc, 20.0, (640, 480))

cap = cv2.VideoCapture(0)
print("💎")

time.sleep(2)
bg = 0

for i in range(60):
    ret, bg = cap.read()

bg = numpy.flip(bg, axis=1)

while cap.isOpened():
    ret, img = cap.read()

    if not ret:
        break

    img = numpy.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = numpy.array([100, 40, 40])
    upper_red = numpy.array([100, 255, 255])

    mask_1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = numpy.array([155, 40, 40])
    upper_red = numpy.array([180, 255, 255])

    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, numpy.ones((3, 3), numpy.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, numpy.ones((3, 3), numpy.uint8))

    mask_2 = cv2.bitwise_not(mask_1)

    res_1 = cv2.bitwise_and(img, img, mask=mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)

    cv2.imshow("Invisibility Cloak", final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
