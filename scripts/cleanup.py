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
REL_ACCOUNT = "account";
ABS_ACCOUNT = os.path.join(ABS_PATH,REL_ACCOUNT);
#TODO 
#maybe automate uploading to google drive
#automation for gathering images is impossible, because this program requires human labor to be able to clasify and preprocess images corectly.

def __main__():

    user = ;
    pswd = ;

    print("name of this batch of images(preferably the date in which they were sent)");
    name = str(input());
    

__main__();
