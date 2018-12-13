import cv2
import numpy as np
import os
import math
import shutil

from scipy import ndimage

#directory="./num_car"
#file_name = 'num_car.png'
directory="./numimg"
file_name='image.png'

directory2="./numimg_conv"

directory3="./numimg_bconv"



if not os.path.exists(directory):
    os.makedirs(directory)

if not os.path.exists(directory2):
    os.makedirs(directory2)

if not os.path.exists(directory3):
    os.makedirs(directory3)

def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted

def convert(cnt):
    filename=directory+"/crop_"+str(cnt)+".jpg"
    gray = cv2.imread(filename)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
   
    (thresh, gray) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV  | cv2.THRESH_OTSU)


    while np.sum(gray[0]) == 0:
        gray = gray[1:]
    while np.sum(gray[:,0]) == 0:
        gray = np.delete(gray,0,1)
    while np.sum(gray[-1]) == 0:
        gray = gray[:-1]
    while np.sum(gray[:,-1]) == 0:
        gray = np.delete(gray,-1,1)

    rows,cols = gray.shape

    if rows > cols:
        factor = 120.0/rows
        rows = 100
        cols = int(round(cols*factor))
        # first cols than rows
        gray = cv2.resize(gray, (cols,rows))
    else:
        factor = 120.0/cols
        cols = 100
        rows = int(round(rows*factor))
        # first cols than rows
        gray = cv2.resize(gray, (cols, rows))

    colsPadding = (int(math.ceil((128-cols)/2.0)),int(math.floor((128-cols)/2.0)))
    rowsPadding = (int(math.ceil((128-rows)/2.0)),int(math.floor((128-rows)/2.0)))
    gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')

    #shiftx,shifty = getBestShift(gray)
    #shifted = shift(gray,shiftx,shifty)
    #gray = shifted

    gray=cv2.bitwise_not(gray)
    gray=cv2.resize(gray,(128,128))    
    filename=directory2+"/crop_"+str(cnt)+".jpg"
    cv2.imwrite(filename , gray)
    #cv2.imwrite(filename , gray)

def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[0] // tolerance_factor) * tolerance_factor) * cols + origin[1]

if __name__ == '__main__':
    box1=[]
    box2=[[0,0,0,0]]
    f_count=0
    select=0
    plate_width=0
    s_x=0
    s_y=0
    
    img=cv2.imread(file_name,cv2.IMREAD_COLOR)
    origin_img=img.copy()
    origin_img2=img.copy()
    copy_img=img.copy()
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img2,(3,3),0)
    #흑백 전처리

    canny=cv2.Canny(blur,100,200)
    #사진에 맞춰준 숫자 100, 200)
    cnts,contours,hierarchy=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt=contours[i]
        area=cv2.contourArea(cnt)
        x,y,w,h=cv2.boundingRect(cnt)
        rect_area=w*h
        aspect_ratio=float(w)/h

        if(aspect_ratio>=0.2) and (aspect_ratio<=1.0) and (rect_area>=150) :
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
            cv2.rectangle(origin_img2,(x,y),(x+w,y+h),(250,255,0),1)
            s5 = '/var/www/html/numrecog/output_origin.jpg'     
            cv2.imwrite(s5 , origin_img2)
            box1.append(cv2.boundingRect(cnt))
   
    #숫자영역 아닌부분 제외
    for i in range(len(box1)):
        for j in range(len(box1)-(i+1)):
            if box1[j][0]>box1[j+1][0]:
                temp=box1[j]
                box1[j]=box1[j+1]
                box1[j+1]=temp
    #오름차순으로 번호판 시작점 찾기
    for m in range(len(box1)):
        count=0
        for n in range(m+1,(len(box1)-1)):
                delta_x=abs(box1[n+1][0]-box1[m][0])
                if(delta_x>150):
                    break;
                delta_y=abs(box1[n+1][1]-box1[m][1])
                if delta_x==0:
                    delta_x=1
                if delta_y==0:
                    delta_y=1
                gradient=float(delta_y)/float(delta_x)
                if gradient<0.25:
                    count=count+1
        if count>f_count:
            select=m
            f_count=count
            plate_width=delta_x

    #s_y=box1[select][1]-10
    #s_x=box1[select][0]-10
    #p_height=abs(box1[select][3]+box1[select][1]+20)
    #p_width=abs(100+box1[select][0])
    #img_nump=cv2.rectangle(img,(s_x,s_y),(delta_x,p_height),(255,255,0),1)
    #s4 = '/var/www/html/numrecog/output_numplate.jpg'     
    #cv2.imwrite(s4 , img_nump)

    number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]-10:140+box1[select][0]]
    #number_plate=copy_img[box1[select][1]-20:box1[select][3]+box1[select][1]+30,box1[select][0]-100:250+box1[select][0]]
    #s2 = '/var/www/html/numrecog/output_numberplate.jpg'     
    #cv2.imwrite(s2 , number_plate)

    #번호판 추출 후
    img  = number_plate
    copy_img=img.copy()
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img2,(3,3),0)
    #흑백 전처리

    canny=cv2.Canny(blur,100,200)
    #사진에 맞춰준 숫자 100, 200)

  
    cnts,contours,hierarchy=cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    contours.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))

    index = 0 
    for contour in contours: 
        x,y,w,h = cv2.boundingRect(contour)

        rect_area=w*h
        aspect_ratio=float(w)/h
  
        if(aspect_ratio>=0.2) and (aspect_ratio<=1.0)  :
            box2.append(cv2.boundingRect(contour))
            cropped = img[y :y +  h , x : x + w]
            #cropped2 = image_final[y :y +  h , x : x + w]   
            if(w>=100):
                    cropped=cv2.resize(cropped,(90,50))        
            s = '/var/www/html/numrecog/numimg/crop_' + str(index) + '.jpg'     
            cv2.imwrite(s , cropped)    
            #s3 = '/var/www/html/numrecog/numimg_bconv/crop_' + str(index) + '.jpg'     
            #cv2.imwrite(s3 , cropped2)    
            index = index + 1
            for i in range(len(box2)):
                cv2.rectangle(origin_img,(box1[select][0]-10+x,box1[select][1]-10+y),(box1[select][0]-10+x+w,box1[select][1]-10+y+h),(255,0,255),1)
    
    s2 = '/var/www/html/numrecog/output.jpg'     
    cv2.imwrite(s2 , origin_img)

    for cnt in range(0,(len(next(os.walk(directory))[2]))):
        convert(cnt)

