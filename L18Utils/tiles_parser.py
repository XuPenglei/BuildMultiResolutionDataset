#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 20:52
# @Author  : XuPenglei
# @Site    : 
# @File    : tiles_parser.py
# @Software: PyCharm
# @email  : xupenglei87@163.com
# @Description: 该程序用来解译91卫图下载的18级影像每个tile的元数据文件

import os
import cv2
from glob import glob
from osgeo import ogr,osr,gdal
from tqdm import tqdm
import numpy as np
from Utils.RasterProcess import RasterProcessor
import json
import skimage.io as io

class MetafileParser():
    def __init__(self,basedir,filename):
        self.img_name = os.path.join(basedir,filename)
        self.tfw_file = os.path.join(basedir,os.path.basename(filename)+'.tfw')
        self.prj_file = os.path.join(basedir,os.path.basename(filename)+'.prj')

    def get_geomat(self):
        with open(self.tfw_file, 'r') as f:
            meta_mat = f.readlines()
        geomat = [float(n.replace('\n', '')) for n in meta_mat]
        formed_geomat = [geomat[-2], geomat[0], 0.0, geomat[-1], 0.0, geomat[3]]
        return formed_geomat

    def get_proj(self):
        with open(self.prj_file,'r') as f:
            proj = f.readline()
        return proj

    def get_extent(self):
        dataset = gdal.Open(self.img_name)
        img_width = dataset.RasterXSize()
        img_height = dataset.RasterYSize()
        geomat = self.get_geomat()
        topleft_lat = geomat[0]
        topleft_lng = geomat[3]
        bottomright_lat = topleft_lat+img_width*geomat[1]
        bottomright_lng = topleft_lng+img_height*geomat[-1]
        return [topleft_lat,bottomright_lat,bottomright_lng,topleft_lng]




