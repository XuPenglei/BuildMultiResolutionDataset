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


