# -*- coding: utf-8 -*-
"""
@ Time    : 2020/7/24 14:26
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : PolygonProcess.py
@ Desc    : 用GDAL处理面数据
"""

from osgeo import gdal,ogr,gdalconst
import os
from tqdm import tqdm
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

ogr.RegisterAll()

class PolyProcessor(object):
    def __init__(self,shp_file):
        self.polys = ogr.Open(shp_file,0)
        if self.polys is None:
            raise FileExistsError
        self.ilayercount = self.polys.GetLayerCount()
        assert self.ilayercount==1

    def attrFilter(self,filt_str):
        """
        属性过滤
        :param filt_str: 过滤字段，与Arcmap属性字段查询相同格式
        :return: 筛选后的图层
        """
        olayer = self.polys.GetLayerByIndex(0)
        # 清除选择
        olayer.ResetReading()
        status = olayer.SetAttributeFilter(filt_str)
        if status==0:
            return olayer
        else:
            print('No record when filt by %s'%(filt_str))

    def rasterize(self,inputLayer,outputfile,templatefile=None,options_dict=None):
        """
        栅格矢量化
        :param inputLayer: 矢量图层
        :param outputfile: 输出文件
        :param templatefile: 模板文件，如果不为None则按模板文件设置否则按options_dict设置
        :param options_dict: 设置字典，包含proj：参考系，interval：每个像素代表的地理间隔
        :return:
        """
        if templatefile:
            data = gdal.Open(templatefile,gdalconst.GA_ReadOnly)
            xSize = data.RasterXSize
            ySize = data.RasterYSize
            proj = data.GetProjection()
            geomat = data.GetGeoTransform()
        else:
            extent = inputLayer.GetExtent()
            ul = extent[:2]
            lr = extent[2:]
            xSize = round((lr[0]-ul[0])/options_dict['interval'])
            ySize = abs(round((lr[1]-ul[1])/options_dict['interval']))
            proj = options_dict['proj']
            geomat = (ul[0],options_dict['interval'],0,ul[1],0,-options_dict['interval'])


        targetDataSet = gdal.GetDriverByName('GTiff').Create(
            outputfile,xSize,ySize,1,gdal.GDT_Byte
        )
        targetDataSet.SetGeoTransform(geomat)
        targetDataSet.SetProjection(proj)
        band = targetDataSet.GetRasterBand(1)
        band.SetNoDataValue(0)
        band.FlushCache()
        gdal.RasterizeLayer(
            targetDataSet,
            [1],
            inputLayer,
            options=["ATTRIBUTE=DN"]
        )

import shutil

def get_outside(inShp, outputShp, field, fieldValue):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(inShp, 1)
    layer = dataSource.GetLayer()

    # 新建DataSource，Layer
    out_ds = driver.CreateDataSource(outputShp)
    out_lyr = out_ds.CreateLayer(outputShp, layer.GetSpatialRef(), ogr.wkbPolygon)
    def_feature = out_lyr.GetLayerDefn()

    for feature in layer:
        geom = feature.GetGeometryRef()
        value = feature.GetField(field)
        if value == fieldValue:
            out_feature = ogr.Feature(def_feature)
            out_feature.SetGeometry(geom)
            out_lyr.CreateFeature(out_feature)
        out_feature = None

    out_ds.FlushCache()
    del dataSource, out_ds


def intersection(maskShp, toInterShp, fname):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(maskShp, 1)
    layer = dataSource.GetLayer()

    RdataSource = driver.Open(toInterShp, 1)
    Rlayer = RdataSource.GetLayer()


    # 新建DataSource，Layer
    out_ds = driver.CreateDataSource(fname)
    out_lyr = out_ds.CreateLayer(fname, Rlayer.GetSpatialRef(), ogr.wkbPolygon)
    def_feature = out_lyr.GetLayerDefn()
    # 遍历原始的Shapefile文件给每个Geometry做Buffer操作
    # current_union = layer[0].Clone()
    print('the length of layer:', len(layer))
    if len(layer) == 0:
        return

    for feature in layer:
        geometry = feature.GetGeometryRef()
        for Rfeature in Rlayer:
            Rgeometry = Rfeature.GetGeometryRef()
            inter = Rgeometry.Intersection(geometry).Clone()
            out_feature = ogr.Feature(def_feature)
            out_feature.SetGeometry(inter)
            out_lyr.ResetReading()
            out_lyr.CreateFeature(out_feature)
    del dataSource, RdataSource, out_ds








if __name__ == '__main__':
    temp_dir = r"F:\Data\2.5TO10\Image91_tif"
    file = r"TFbeijing229_4585.tif"
    out_dir = r"F:\Data\2.5TO10\BuildGT91"
    filt_str = "GridName = '%s'"%(file.split('.')[0])
    polyProcessor = PolyProcessor(r'F:\Data\trainSHP\TFbeijing_Inter.shp')
    polyLayer = polyProcessor.attrFilter(filt_str)
    polyProcessor.rasterize(polyLayer,os.path.join(out_dir,file),os.path.join(temp_dir,file))
    data = io.imread(os.path.join(out_dir,file))
    plt.imshow(data)
    plt.show()


