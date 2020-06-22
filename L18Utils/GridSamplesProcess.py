# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/22 8:02
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : GridSamplesProcess.py
@ Desc    : 本程序用于处理与哨兵二号对应网格的数据，使用重合网格的shp文件下载了对应区域的影像，但是文件名与原始数据有差距
"""

import os
import shutil
from glob import glob
from osgeo import ogr,osr,gdal
from  tqdm import tqdm

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

if __name__ == '__main__':
    IMG91Dir = r'F:\Data\2.5TO10\TiandiImage'
    newDir = r'F:\Data\2.5TO10\Image91_tif'
    shpDir = r'F:\Data\2.5TO10\SamplesShp\GroupWiseShp'
    RenameAndMoveFile(IMG91Dir,newDir,shpDir)