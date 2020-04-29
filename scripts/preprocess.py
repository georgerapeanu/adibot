#!/usr/bin/python3

import cv2;
import os;
import matplotlib.pyplot as plt;
import numpy as np;

IMAGE_DIR = "../images"
OUTPUT_DIR = "../images_output"

def __main__():

    for filename in os.listdir(IMAGE_DIR):
        if(filename.endswith(".jpg")):
            im = cv2.imread(os.path.join(IMAGE_DIR,filename));
            thresh = cv2.inRange(im,(93,84,96),(255,255,255));
            thresh_rgb = cv2.cvtColor(thresh,cv2.COLOR_GRAY2RGB);
            print(filename);
            contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            bst_rect = [];bst_area = 0;

            for contour in contours:
                rect = cv2.minAreaRect(contour);
                center,size,theta = rect;
                if(size[0] * size[1] > bst_area):
                    bst_rect = rect;
                    bst_area = size[0] * size[1];

           
            center,size,theta = bst_rect;
            center,size = tuple(map(int,center)),tuple(map(int,size));
            if(theta + 45 < 0):
                theta = theta + 90;
                size = (size[1],size[0]);
            elif(theta - 45 > 0):
                theta = theta - 90;
                size = (size[1],size[0]);

            bordersize = int(max(im.shape[0],im.shape[1]) / 2 + 1);
            im = cv2.copyMakeBorder(im,top=bordersize,bottom=bordersize,left=bordersize,right=bordersize,borderType=cv2.BORDER_CONSTANT,value = [0,0,0])
            center = (center[0] + bordersize,center[1] + bordersize);
            M = cv2.getRotationMatrix2D( center, -theta, 1)
            big_dist = (im.shape[0] ** 2 + im.shape[1] ** 2) ** 0.5;
            extract = cv2.warpAffine(im, M, (int(big_dist),int(big_dist)));
            extract = cv2.getRectSubPix(extract, size, center);
            
            cv2.imwrite(os.path.join(OUTPUT_DIR,filename),extract);

__main__();
