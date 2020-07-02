# -*- coding: utf-8 -*-
"""
@ Time    : 2020/7/2 14:47
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : resampleL18ToSentinel2.py
@ Desc    : 将L18的影像resample到和ST2一样的分辨率
"""
from osgeo import gdal,osr,ogr
from osgeo.gdalconst import *
import numpy as np
import cv2
from skimage.io import imread,imsave
import os
from glob import glob
from Utils.RasterProcess import RasterProcessor

def processSingle(p,img_path,out_dir,w,h):
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
    new_raster,new_geomat = p.resampleWithGeo(raster, geomat, w=w,h=h)
    new_path = os.path.join(out_dir,os.path.basename(img_path))
    imsave(new_path,new_raster)
    del new_raster,raster
    new_gdal_data = gdal.Open(new_path,GA_Update)
    new_gdal_data.SetProjection(proj)
    new_gdal_data.SetGeoTransform(new_geomat)
    del new_gdal_data,gdal_data

def SetProjAndGeomat(path,proj,geomat):
    gdal_data = gdal.Open(path,GA_Update)
    gdal_data.SetProjection(proj)
    gdal_data.SetGeoTransform(geomat)
    del gdal_data


if __name__ == '__main__':
    img_dir= r'F:\Data\ZT_SRDataset\四个定量精度评价区\IMG_L18'
    img_paths = glob(os.path.join(img_dir,'*.tif'))
    out_dir = r'F:\Data\ZT_SRDataset\四个定量精度评价区\IMG2p5'
    purpose_dir = r'F:\Data\ZT_SRDataset\四个定量精度评价区\GT2p5TF'
    p = RasterProcessor()
    # for path in img_paths:
    #     fn = os.path.basename(path)
    #     print('Processing ',fn)
    #     purpose_data = gdal.Open(os.path.join(purpose_dir,fn))
    #
    #
    #     if purpose_data is None:
    #         raise ValueError
    #     w,h = purpose_data.RasterXSize, purpose_data.RasterYSize
    #     del purpose_data
    #     processSingle(p,path,out_dir,w,h)

    for path in img_paths:
        fn = os.path.basename(path)
        print('Processing ', fn)
        purpose_data = gdal.Open(os.path.join(purpose_dir, fn))
        geomat = purpose_data.GetGeoTransform()
        proj = purpose_data.GetProjection()
        if purpose_data is None:
            raise ValueError
        del purpose_data
        SetProjAndGeomat(os.path.join(out_dir,fn),proj,geomat)



