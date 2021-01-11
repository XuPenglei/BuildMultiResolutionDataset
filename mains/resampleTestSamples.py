#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/10 15:31
# @Author  : XuPenglei
# @Site    : 
# @File    : resampleTestSamples.py
# @Software: PyCharm
# @email  : xupenglei87@163.com
# @Description: 将测试数据重采样到应该有的尺度

from osgeo import gdal,osr,ogr
from osgeo.gdalconst import *
import numpy as np
import cv2
from skimage.io import imread,imsave
import os
from glob import glob
from Utils.RasterProcess import RasterProcessor

def processSingle(p,img_path,out_dir,w,h,inter):
    """
    处理一个图片
    :param img_path:
    :param out_dir: 输出文件夹
    :param w: 目标w
    :param h: 目标h
    :return:
    """
    gdal_data = gdal.Open(img_path)
    if gdal_data is None:
        raise ValueError
    geomat = gdal_data.GetGeoTransform()
    proj = gdal_data.GetProjection()
    raster = imread(img_path,plugin='gdal')
    new_raster,new_geomat = p.resampleWithGeo(raster, geomat, w=w,h=h,inter=inter)
    new_path = os.path.join(out_dir,os.path.basename(img_path))
    imsave(new_path,new_raster)
    del new_raster,raster
    new_gdal_data = gdal.Open(new_path,GA_Update)
    new_gdal_data.SetProjection(proj)
    new_gdal_data.SetGeoTransform(new_geomat)
    del new_gdal_data,gdal_data

if __name__ == '__main__':
    SR = 8
    img_dir = r'Z:\Data\dataset\hr\label\test'
    img_paths = glob(os.path.join(img_dir, '*.tif'))
    out_dir = r'Z:\Data\dataset\hr\label\testX%d'%SR
    p = RasterProcessor()
    inter = cv2.INTER_NEAREST
    for path in img_paths:
        fn = os.path.basename(path)
        print('Processing ',fn)
        w,h = 1416*SR, 1437*SR
        processSingle(p,path,out_dir,w,h,inter)