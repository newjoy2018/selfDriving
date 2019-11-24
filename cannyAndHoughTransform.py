import cv2
import numpy as np

img = cv2.imread('test_lane.jpg')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel_size = 3
blur_gray = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)
edges = cv2.Canny(img_gray, 10, 200)
#lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)
line_image = np.copy(img) * 0
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 1, np.array([]),10, 5)
print(lines.shape)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),3)

color_edges = np.dstack((edges, edges, edges))

combin = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 


# cv2.imshow('img_gray', img_gray)
# cv2.imshow('blur_gray', blur_gray)
cv2.imshow('Combination of Edges and Lines', combin)
cv2.waitKey(0)
cv2.destroyAllWindows()
