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
ABS_PROBLEME = os.path.join(ABS_IMAGES,REL_PROBLEME);
ABS_SOLUTII = os.path.join(ABS_IMAGES,REL_SOLUTII);
REL_OUTPUT = "images_out";
ABS_OUTPUT = os.path.join(ABS_PATH,REL_OUTPUT);
REL_TMP = "tmp";
ABS_TMP = os.path.join(ABS_PATH,REL_TMP);

RESCALE_FACTOR = 3;

mouse_x = 0;
mouse_y = 0;

def mouse_click(event,x,y,flags,param):
    global mouse_x,mouse_y;
    mouse_x = x;
    mouse_y = y;

#TODO 
#merge problems with coresponding solutions and output them
#maybe automate uploading to google drive
#automation for gathering images is impossible, because this program requires human labor to be able to clasify and preprocess images corectly.
def crop_to_points(im,points):
    for i in range(0,len(points)):
        points[i] = (points[i][1] * RESCALE_FACTOR,points[i][0] * RESCALE_FACTOR);#because on image.shape the x axes is the height. but its weird because this happens only in image.shape,the rest has normal XOY
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
    print("processing theory...");
    preprocess.process(ABS_TEORIE,ABS_TMP);
    cnt = 1;
    for filename in sorted(os.listdir(ABS_TMP)):
        if filename.endswith(".jpg"):
            im = cv2.imread(os.path.join(ABS_TMP,filename));
            cv2.imwrite(os.path.join(ABS_OUTPUT,"teorie" + str(cnt) + ".jpg"),im);
            cnt = int(cnt) + 1;
    subprocess.call("rm " + ABS_TMP + " -r",shell = True);


    print("processing problems...");
    os.mkdir(ABS_TMP);
    preprocess.process(ABS_PROBLEME,ABS_TMP);
    cnt = 1;
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',mouse_click)
    problems = [];
    for filename in sorted(os.listdir(ABS_TMP)):
        if True or filename.endswith(".jpg"):
            im = cv2.imread(os.path.join(ABS_TMP,filename));
            points = [];
            while(True):
                tmp = np.array(im);
                tmp = cv2.resize(im,(int(tmp.shape[1] / RESCALE_FACTOR),int(tmp.shape[0] / RESCALE_FACTOR)));#same reason here,idk why
                if(len(points) > 0):
                    cv2.drawContours(tmp,np.array([np.array(points)]),0,(255,0,0),3);
                cv2.imshow("image",tmp);
                k = cv2.waitKey();
                if k == ord('s'):
                    if len(problems) > 0 and problems[len(problems) - 1][0] == cnt:
                        tmp2 = np.array(problems[len(problems) - 1][1]);
                        w = max(tmp2.shape[1],im.shape[1]);
                        tmp2 = cv2.resize(tmp2,(w,tmp2.shape[0]));
                        im = cv2.resize(im,(w,im.shape[0]));
                        problems[len(problems) - 1] = (cnt,cv2.vconcat([tmp2,im]));
                    else:
                        problems.append((cnt,im));
                    break;
                elif k == ord('a'):
                    points.append((mouse_x,mouse_y));
                elif k == ord('u'):
                    points = points[:-1:]
                elif k == ord('d'):
                    extract,im = crop_to_points(im,points);                
                    if len(problems) > 0 and problems[len(problems) - 1][0] == cnt:
                        tmp2 = np.array(problems[len(problems) - 1][1]);
                        w = max(tmp2.shape[1],extract.shape[1]);
                        tmp2 = cv2.resize(tmp2,(w,tmp2.shape[0]));
                        extract = cv2.resize(extract,(w,extract.shape[0]));
                        print(tmp2.shape,extract.shape);
                        problems[len(problems) - 1] = (cnt,cv2.vconcat([tmp2,extract]));
                    else:
                        problems.append((cnt,extract));
                    cnt = cnt + 1;
                    points = [];

    subprocess.call("rm " + ABS_TMP + " -r",shell = True);
    cv2.destroyAllWindows();
    
    print("processing solutions...");
    os.mkdir(ABS_TMP);
    preprocess.process(ABS_SOLUTII,ABS_TMP);
    cnt = 1;
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',mouse_click)
    solutions = [];
    for filename in sorted(os.listdir(ABS_TMP)):
        if True or filename.endswith(".jpg"):
            im = cv2.imread(os.path.join(ABS_TMP,filename));
            points = [];
            while(True):
                tmp = np.array(im);
                tmp = cv2.resize(im,(int(tmp.shape[1] / RESCALE_FACTOR),int(tmp.shape[0] / RESCALE_FACTOR)));#same reason here,idk why
                if(len(points) > 0):
                    cv2.drawContours(tmp,np.array([np.array(points)]),0,(255,0,0),3);
                cv2.imshow("image",tmp);
                k = cv2.waitKey();
                if k == ord('s'):
                    if len(solutions) > 0 and solutions[len(solutions) - 1][0] == cnt:
                        tmp2 = np.array(solutions[len(solutions) - 1][1]);
                        w = max(tmp2.shape[1],im.shape[1]);
                        tmp2 = cv2.resize(tmp2,(w,tmp2.shape[0]));
                        im = cv2.resize(im,(w,im.shape[0]));
                        solutions[len(solutions) - 1] = (cnt,cv2.vconcat([tmp2,im]));
                    else:
                        solutions.append((cnt,im));
                    break;
                elif k == ord('a'):
                    points.append((mouse_x,mouse_y));
                elif k == ord('u'):
                    points = points[:-1:]
                elif k == ord('d'):
                    extract,im = crop_to_points(im,points);                
                    if len(solutions) > 0 and solutions[len(solutions) - 1][0] == cnt:
                        tmp2 = np.array(solutions[len(solutions) - 1][1]);
                        w = max(tmp2.shape[1],extract.shape[1]);
                        tmp2 = cv2.resize(tmp2,(w,tmp2.shape[0]));
                        extract = cv2.resize(extract,(w,extract.shape[0]));
                        print(tmp2.shape,extract.shape);
                        solutions[len(solutions) - 1] = (cnt,cv2.vconcat([tmp2,extract]));
                    else:
                        solutions.append((cnt,extract));
                    cnt = cnt + 1;
                    points = [];

    cnt = 0;

    for i in range(0,max(len(solutions),len(problems))):
        cnt = cnt + 1;
        if(i >= len(solutions)):
            cv2.imwrite(os.path.join(ABS_OUTPUT,"problema" + str(cnt) + ".jpg"),problems[i][1]);
        elif(i >= len(problems)):
            cv2.imwrite(os.path.join(ABS_OUTPUT,"solutia" + str(cnt) + ".jpg"),solutions[i][1]);
        else:
            w = max(problems[i][1].shape[1],solutions[i][1].shape[1]);
            prob = cv2.resize(problems[i][1],(w,problems[i][1].shape[0]));
            sol = cv2.resize(solutions[i][1],(w,solutions[i][1].shape[0]));
            im = cv2.vconcat([prob,sol]);
            cv2.imwrite(os.path.join(ABS_OUTPUT,"problema+solutia" + str(cnt) + ".jpg"),im);

    subprocess.call("rm " + ABS_TMP + " -r",shell = True);
    cv2.destroyAllWindows();
__main__();
