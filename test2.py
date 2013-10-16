#coding=utf-8
import cv2
import numpy as np

img = cv2.imread("IMAG1857.jpg",0)
leny = 800
lenx = int(float(img.shape[0])/img.shape[1]*leny)
img = cv2.resize(img, (leny, lenx))

img = cv2.GaussianBlur(img, (3,3), 0)
edges = cv2.Canny(img, 50, 150, apertureSize = 3)
#lines = cv2.HoughLines(edges,1,np.pi/180,118)   #这里最后一个参数使用了经验型的值
#result = img.copy()


# 经验参数
minLineLength = 200
maxLineGap = 15 
lines = cv2.HoughLinesP(edges, 1, np.pi/180,80,minLineLength,maxLineGap)

for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(2,255,0),2)

#cv2.imshow('Canny', edges)
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
