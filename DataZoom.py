'''
@Author: your name
@Date: 2020-04-27 07:54:44
@LastEditTime: 2020-04-27 08:43:06
@LastEditors: Please set LastEditors
@Description: 将图片缩放到不同的分辨率
@FilePath: \BuildMultiResolutionDataset\DataZoom.py
'''
import cv2
import numpy as np 
import os

def zoom(img,zoom_rate,out_path=None,rezoom=True):
    result = cv2.resize(img,None,fx=1/zoom_rate,fy=1/zoom_rate)
    if rezoom:
        result = cv2.resize(result,None,fx=zoom_rate,fy=zoom_rate)
    cv2.imshow(str(zoom_rate),result)
    cv2.waitKey(0)
    if out_path:
        cv2.imwrite(os.path.join(out_path,'x_%d.png'%(zoom_rate)),result)


src = cv2.imread(r'C:\Users\XuPenglei\Desktop\data_clip\clip.tif')[500:,500:]
for l in [1,2,4,8,16]:
    zoom(src,l,r'C:\Users\XuPenglei\Desktop\data_clip',rezoom=False)

# src = cv2.imread(r'C:\Users\XuPenglei\Desktop\test\17-12-6\ditu(0)\Level18\ditu(0).tif',1)
# clip = src[4000:4500,4000:4500,:]
# clipx2 = cv2.resize(clip,None,fx=0.5,fy=0.5)
# clipx4 = cv2.resize(clip,None,fx=0.25,fy=0.25)
# cv2.imshow('clip',clip)
# cv2.imshow('x2',clipx2)
# cv2.imshow('x4',clipx4)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
