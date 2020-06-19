# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/19 9:20
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : StatisticsGF2Extent.py
@ Desc    : 本代码用于统计组内GF2数据的范围及其他信息,数据Dell工作站
"""

from osgeo import gdal,ogr,osr
import json
from glob import glob
import os

def writeJson(data,path):
    with open(path,'w') as f:
        json.dump(data,f)
    print('Write Json Successfully!')

def ReadJson(path):
    with open(path,'r') as f:
        data = json.load(f)
    return data


def GetSingleRasterInfo(data):
    """
    获取单个栅格的信息
    :param data: 栅格数据，由gdal.Open打开
    :return: infoDict
    """
    name = data.GetDescription()
    projWKT = data.GetProjection()
    geoMAT = data.GetGeoTransform()
    w,h = data.RasterXSize, data.RasterYSize
    ulLon,ulLat = geoMAT[0],geoMAT[3]
    brLon,brLat = ulLon+w*geoMAT[1],ulLat+h*geoMAT[5]
    # 投影坐标转化为空间坐标
    sourceProj = osr.SpatialReference()
    sourceProj.ImportFromWkt(projWKT)
    targetProj = osr.SpatialReference()
    targetProj.ImportFromEPSG(4326)
    ct = osr.CoordinateTransformation(sourceProj,targetProj)
    if 'UTM' in projWKT:
        ulLatWGS, ulLonWGS, _ = ct.TransformPoint(ulLon, ulLat)
        brLatWGS, brLonWGS, _ = ct.TransformPoint(brLon, brLat)
    else:
        ulLonWGS,ulLatWGS,_ = ct.TransformPoint(ulLon,ulLat)
        brLonWGS,brLatWGS,_ = ct.TransformPoint(brLon,brLat)


    return dict(name=name,projWKT=projWKT,geoMAT=geoMAT,
                OriExtent=[ulLon,ulLat,brLon,brLat],
                WGSExtent=[ulLonWGS,ulLatWGS,brLonWGS,brLatWGS])

def GetInfoFromFolder(folder):
    """
    从文件夹中统计所有文件相关tif的信息
    :param folder: 需要统计的文件夹，组织形式为 folder/subfolder/tif
    :return: infoDict: {city:[dict,dict,...]}
    """
    dirList = [d for d in os.listdir(folder) if 'GF2' in d]
    infoDict = {}
    for d in dirList:
        city = d.split('_')[0]
        tifPath = glob(os.path.join(folder,d,'*FUSION.tif'))[0]
        data = gdal.Open(tifPath)
        if data is not None:
            rasterINFO = GetSingleRasterInfo(data)
            rasterINFO.update({'path':tifPath})
        else:
            raise ValueError
        if city in infoDict.keys():
            infoDict[city].append(rasterINFO)
        else:
            infoDict.update({city:[rasterINFO]})
    data = None

    return infoDict

if __name__ == '__main__':
    folder = r'D:\组内数据汇总\GF2_building'
    outJson = r'GF2Info.json'
    InfoDict = GetInfoFromFolder(folder)
    writeJson(InfoDict,outJson)










