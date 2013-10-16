#coding=utf-8
import cv2
import numpy as np  
import sys

def DetectLine(imgname):
    img = cv2.imread(imgname)
    leny = 800
    lenx = int(float(img.shape[0])/img.shape[1]*leny)
    img = cv2.resize(img, (leny, lenx))
    
    
    img = cv2.GaussianBlur(img,(3,3),0)
    edges = cv2.Canny(img, 100, 280, apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,118)
    result = img.copy()
    
    cv2.imshow('Canny', edges)
    cv2.waitKey(0)
    
    #经验参数
    try:
        lines = cv2.HoughLinesP(edges,1, np.pi/180, 100, minLineLength = 170, maxLineGap = 150)
        for x1,y1,x2,y2 in lines[0]:
        	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    
        cv2.imshow('Result', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print imgname, len(lines[0]), '\n'
    except:
        print "ERR\n"

if __name__ == "__main__":
    for i in range(1,len(sys.argv)):
        filename = sys.argv[i]
        if filename[-4:] in ['.jpg',]:
            DetectLine(filename)
