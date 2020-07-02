# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/22 8:02
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : GridSamplesProcess.py
@ Desc    : 本程序用于处理与哨兵二号对应网格的数据，使用重合网格的shp文件下载了对应区域的影像，但是文件名与原始数据有差距
"""

import os
import cv2
import shutil
from glob import glob
from osgeo import ogr,osr,gdal
from tqdm import tqdm
import numpy as np
from Utils.RasterProcess import RasterProcessor
import json
import skimage.io as io

def readFromSingleShp(file):
    """
    从单个shp中读取每条记录的信息
    :param file: shp路径
    :return: record: 返回字典，{91卫图下载名:对应哨兵2号样本名}
    """
    ds = ogr.Open(file,False)
    layer = ds.GetLayer(0)
    lydefn = layer.GetLayerDefn()
    spatialref = layer.GetSpatialRef()
    geomtype = lydefn.GetGeomType()
    fieldlist = []
    for i in range(lydefn.GetFieldCount()):
        fddefn = lydefn.GetFieldDefn(i)
        fddict = {'name':fddefn.GetName(),
                  'type':fddefn.GetType(),
                  'width':fddefn.GetWidth(),
                  'decimal':fddefn.GetPrecision()}
        fieldlist+=[fddict]
    record = {}
    n = 0
    shp_name = os.path.basename(file).split('.')[0]
    feature = layer.GetNextFeature()
    while feature is not None:
        name = shp_name + '_' + 'part%d'%(n)
        sentinel2Name = feature.GetField('GridName')
        record.update({name:sentinel2Name})
        n+=1
        feature=layer.GetNextFeature()
    ds.Destroy()
    return record

def RenameAndMoveFile(IMG91Dir,newDir, shpDir):
    """
    将sentinel样本对应的数据重命名并转移到其他文件夹
    :param IMG91Dir: 91卫图的下载路径
    :param newDir: 转移路径
    :param shpDir: 91卫图下载用到的shp文件路径
    :return:
    """
    shpList = glob(os.path.join(shpDir,'*.shp'))
    for shp in shpList:
        print('Processing %s'%(shp))
        shpName = os.path.basename(shp).split('.')[0]
        oldDir = os.path.join(IMG91Dir,shpName,'Level18')
        mapDict = readFromSingleShp(shp)
        for k,v in tqdm(mapDict.items()):
            oldName = os.path.join(oldDir,k+'.tif')
            newName = os.path.join(newDir,v+'.tif')
            shutil.copyfile(oldName,newName)

def ResizeRasters(rasterfolder,outfolder,size,factor=None):
    """
    将文件夹下所有图片resize到固定大小
    :param rasterfolder: 源文件夹
    :param outfolder: 目标文件夹
    :param size: 需要resize的大小
    :param factor: 需要resize的比率，如果不为None,size应为0
    :return:
    """
    img_list = glob(os.path.join(rasterfolder,'*.tif'))
    processor = RasterProcessor()
    for img in tqdm(img_list):
        img_name = os.path.basename(img)
        out_path = os.path.join(outfolder,img_name)
        imgArr = cv2.imread(img,-1)
        if imgArr is not None:
            resizeIMG = processor.resample(imgArr,256,256)
            cv2.imwrite(out_path,resizeIMG)
        else:
            raise ValueError

def scale0to1(rasterfolder,npyfolder,max=255,min=0):
    """
    将图片变为0到1之间并保存为npy文件
    :param rasterfolder: 栅格文件夹
    :param npyfolder: npy文件夹
    :param max: 栅格最大值
    :param min: 栅格最小值
    :return:
    """
    img_list = glob(os.path.join(rasterfolder, '*.tif'))
    processor = RasterProcessor()
    for img in tqdm(img_list):
        img_name = os.path.basename(img)
        out_path = os.path.join(npyfolder, img_name.replace('.tif','.npy'))
        imgArr = cv2.imread(img, -1)
        if imgArr is not None:
            scaleIMG = processor.maxminScale(imgArr, 255, 0)
            np.save(out_path,scaleIMG)
        else:
            raise ValueError

def clipCloudFromExtent(rasterfolder,outfolder,extentJson,wh):
    """
    从extentJson记录的范围中在对应栅格上裁剪带云的数据
    :param rasterfolder: 整图的文件夹
    :param outfolder: 保存文件夹
    :param extentJson: 范围json
    :return:
    """
    processor = RasterProcessor()
    with open(extentJson,'r') as f:
        extent = json.load(f)
    cloudExtent = [d for d in extent.keys() if 'cloud' in d]
    nanjingCloud = [d for d in cloudExtent if 'nanjing' in d]
    kunmingCloud = [d for d in cloudExtent if 'kunming' in d]
    nanjingP = os.path.join(rasterfolder,'TFnanjing.tif')
    kunmingP = os.path.join(rasterfolder,'TFkunming.tif')
    nanjingGeomat = gdal.Open(nanjingP).GetGeoTransform()
    kunmingGeomat = gdal.Open(kunmingP).GetGeoTransform()
    nanjingraster = io.imread(nanjingP)
    for e in tqdm(nanjingCloud):
        ext = extent[e]
        cliped_raster = (processor.clipWithGeo(nanjingraster,ext[0:2],ext[2:4],nanjingGeomat,wh)-1)*255
        print(cliped_raster.shape)
        io.imsave(os.path.join(outfolder,e+'_HR.png'),arr=cliped_raster)
    del nanjingraster
    kunmingraster = io.imread(kunmingP)
    for e in tqdm(kunmingCloud):
        ext = extent[e]
        cliped_raster = (processor.clipWithGeo(kunmingraster,ext[0:2],ext[2:4],kunmingGeomat,wh)-1)*255
        assert cliped_raster.shape[0]==cliped_raster.shape[1]==256
        io.imsave(os.path.join(outfolder,e+'_HR.png'),arr=cliped_raster)





if __name__ == '__main__':
    """    # 改名并移到其他文件夹
    IMG91Dir = r'F:\Data\2.5TO10\TiandiImage'
    newDir = r'F:\Data\2.5TO10\Image91_tif'
    shpDir = r'F:\Data\2.5TO10\SamplesShp\GroupWiseShp'
    RenameAndMoveFile(IMG91Dir,newDir,shpDir)"""

    """# 图片大小重采样
    origin91SampleDir = r'F:\Data\2.5TO10\Image91_tif'
    resample91Dir = r'F:\Data\2.5TO10\Image91_256_tif'
    ResizeRasters(origin91SampleDir,resample91Dir,256)"""

    """# 归一化保存为npy文件
    imgDir = r'F:\Data\2.5TO10\Image91_256_tif'
    npyDir = r'F:\Data\2.5TO10\Image91_256_scaledNPY'
    scale0to1(imgDir,npyDir)"""

    # 裁剪带云影像对应区域HR的无云2.5mGT
    raster_folder = r'F:\Data\2.5TO10\数据说明及地理信息找回\testIMG\Build2p5GeoTif'
    out_folder = r'F:\Data\2.5TO10\数据说明及地理信息找回\testIMG\CloudExtent2p5'
    extentJson = r'F:\Data\2.5TO10\数据说明及地理信息找回\AllSamplesGeoExtent.json'
    clipCloudFromExtent(raster_folder,out_folder,extentJson,[256,256])