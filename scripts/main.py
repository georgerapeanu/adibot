#!/usr/bin/python3

import cv2;
import preprocess;
import numpy as np;
import os;
import subprocess;

ABS_PATH = os.path.dirname(os.path.abspath(os.getcwd()));
REL_IMAGES = "images"
ABS_IMAGES = os.path.join(ABS_PATH,REL_IMAGES);
REL_TEORIE = "teorie";
REL_PROBLEME = "probleme";
REL_SOLUTII = "solutii";
ABS_TEORIE = os.path.join(ABS_IMAGES,REL_TEORIE);
ABS_PROBLEME = os.path.join(ABS_IMAGES,REL_SOLUTII);
ABS_SOLUTII = os.path.join(ABS_IMAGES,REL_PROBLEME);
REL_OUTPUT = "images_out";
ABS_OUTPUT = os.path.join(ABS_PATH,REL_OUTPUT);
REL_TMP = "tmp";
ABS_TMP = os.path.join(ABS_PATH,REL_TMP);

mouse_x = 0;
mouse_y = 0;

def mouse_click(event,x,y,flags,param):
    global mouse_x,mouse_y;
    mouse_x = x;
    mouse_y = y;

#TODO resize image before cv2.imshow() so it fits on screen.
#do the same thing we do on problems on solutions
#merge problems with coresponding solutions and output them
#maybe automate uploading to google drive
#automation for gathering images is impossible, because this program requires human labor to be able to clasify and preprocess images corectly.
def crop_to_points(im,points):
    for i in range(0,len(points)):
        points[i] = (points[i][1],points[i][0]);#because on image.shape the x axes is the height. but its weird because this happens only in image.shape,the rest has normal XOY
    #i dont know tbh, it just works this way
    a = float(points[1][0] - points[0][0]) / (points[1][1] - points[0][1]);
    b = points[1][0] - a * points[1][1];
    points[0] = (int(b),0);
    points[1] = (int(im.shape[1] * a + b),im.shape[1])
    points.append((0,im.shape[1]));
    points.append((0,0));
    for i in range(0,len(points)):
        points[i] = (points[i][1],points[i][0]);#swap back
        
    mask = np.ones(im.shape,dtype = np.uint8);
    mask.fill(255);
    roi_corners = np.array([np.array(points,dtype = np.int32)], dtype=np.int32)
    cv2.fillPoly(mask, roi_corners, 0);
    extract = cv2.bitwise_or(im,mask);
    new_im = cv2.bitwise_or(im,cv2.bitwise_not(mask));

    extract = extract[0:max(points[0][1],points[1][1]),0:im.shape[1]]
    new_im = new_im[min(points[0][1],points[1][1]):im.shape[0],0:im.shape[1]]

    return (extract,new_im)

def __main__():
    global mouse_x,mouse_y;
    if(os.path.exists(ABS_TMP) == True):
       subprocess.call("rm " + ABS_TMP + " -r",shell = True);
    os.mkdir(ABS_TMP);
    preprocess.process(ABS_TEORIE,ABS_TMP);
    cnt = 1;
    for filename in sorted(os.listdir(ABS_TMP)):
        if filename.endswith(".jpg"):
            im = cv2.imread(os.path.join(ABS_TMP,filename));
            cv2.imwrite(os.path.join(ABS_OUTPUT,"teorie" + str(cnt) + ".jpg"),im);
            cnt = int(cnt) + 1;
    subprocess.call("rm " + ABS_TMP + " -r",shell = True);

    os.mkdir(ABS_TMP);
    preprocess.process(ABS_PROBLEME,ABS_TMP);
    cnt = 1;
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',mouse_click)
    problems = [];
    for filename in sorted(os.listdir(ABS_TMP)):
        if filename.endswith(".jpg"):
            im = cv2.imread(os.path.join(ABS_TMP,filename));
            points = [];
            while(True):
                tmp = np.array(im);
                if(len(points) > 0):
                    cv2.drawContours(tmp,np.array([np.array(points)]),0,(255,0,0),3);
                cv2.imshow("image",tmp);
                k = cv2.waitKey();
                if k == ord('s'):
                    problems.append((cnt,im));
                    break;
                elif k == ord('a'):
                    points.append((mouse_x,mouse_y));
                elif k == ord('u'):
                    points = points[:-1:]
                elif k == ord('d'):
                    #cv2.drawContours(im,np.array([np.array(points)]),0,(255,0,0),3);
                    extract,im = crop_to_points(im,points);                
                    problems.append((cnt,extract));
                    cv2.imshow("pula",extract);
                    cnt = cnt + 1;
                    points = [];

    subprocess.call("rm " + ABS_TMP + " -r",shell = True);
    cv2.destroyAllWindows();
__main__();
