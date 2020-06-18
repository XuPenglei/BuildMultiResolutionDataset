#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   GetBuildingFromZTmap.py
@Time    :   2020/06/01 07:38:06
@Author  :   Xu Penglei 
@Version :   1.0
@Contact :   xupenglei87@163.com
@Desc    :   本程序是将已经从天地图上提取到的建筑物标签再进行提存，去除小的斑块，同时转化为shp文件
'''

# here put the import lib
import glob
import numpy as np
import multiprocessing.dummy as multiprocessing
from osgeo import gdal,ogr,gdal_array
import matplotlib.pyplot as plt



def getExtent(data):
    """ 获取栅格数据的范围 """
    xSize, ySize = data.RasterXSize, data.RasterYSize
    trans_mat = data.GetGeoTransform()
    tl = [trans_mat[0],trans_mat[3]]
    rd = [trans_mat[0]+(xSize)*trans_mat[1]+(xSize)*trans_mat[2],
            trans_mat[3]+(ySize)*trans_mat[4]+(ySize)*trans_mat[5]]
    return tl,rd

def SieveMask(data,filt_dic=None):
    
    src_band = data.GetRasterBand(1)
    dst_band = src_band
    result = gdal.SieveFilter(src_band, None, dst_band, filt_dic['thresold'],filt_dic['connectness'])

    return dst_band

def save_SieveMask(outpath,data,img_type='GTiff',filt=True,filt_dic=None):
    driver = gdal.GetDriverByName(img_type)
    im_proj = data.GetProjection()
    transform_mat = data.GetGeoTransform()
    wh = [data.RasterXSize, data.RasterYSize]
    arr = (data.GetRasterBand(1).ReadAsArray()==255).astype(np.byte)
    new_raster = driver.Create(outpath,wh[0],wh[1],
                              1,gdal.GDT_Byte)
    new_raster.SetGeoTransform(transform_mat)
    new_raster.SetProjection(im_proj)
    raster_band = new_raster.GetRasterBand(1)
    raster_band.WriteArray(arr)
    if filt:
        _ = gdal.SieveFilter(raster_band,None,raster_band,filt_dic['thresold'],filt_dic['connectness'])


def Polygonize(srcband,out_shp_path):
    maskband = srcband.GetMaskBand()
    drv = ogr.GetDriverByName('ESRI Shapefile')
    dst_ds = drv.CreateDataSource(out_shp_path)
    srs = None
    dst_layername = 'label'
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    dst_fieldname = 'DN'
    fd = ogr.FieldDefn(dst_fieldname,ogr.OFTInteger)
    dst_layer.CreateField(fd)
    dst_field = 0
    options = []
    gdal.Polygonize(srcband,maskband,dst_layer,
                dst_field, options)


def Raster2Poly(tif_path, out_shp_path):
    """ 矢量化栅格 """
    ds = gdal.Open(tif_path, gdal.GA_ReadOnly)
    if not ds:
        print('%s 打开失败' % (tif_path))
        return
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()

    drv = ogr.GetDriverByName('ESRI Shapefile')
    dst_ds = drv.CreateDataSource(out_shp_path)
    srs = None
    dst_layername = 'label'
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    dst_fieldname = 'DN'
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    dst_field = 0
    options = []
    gdal.Polygonize(srcband, maskband, dst_layer, dst_field, options)

if __name__ == "__main__":
    raster_file = r"F:\Data\tiandiIMG\TiandiMap\TFbeijingMap.tif"
    out_tif = r"F:\Data\tiandiIMG\SievedTiandiMap\Beijing.tif"
    data = gdal.Open(raster_file)
    extent = getExtent(data)
    print(extent)
    filt_dic=dict(thresold=150,connectness=4)
    # sieved = save_SieveMask(out_tif, data,'GTiff',True,filt_dic)
    Raster2Poly(out_tif,r"F:\Data\tiandiIMG\TiandiMap_shp\Beijing.shp")