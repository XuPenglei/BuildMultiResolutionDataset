# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/18 14:49
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : makeShp.py
@ Desc    : 从其他文件格式中生成Shp文件
"""

try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except:
    import gdal
    import ogr
import os
import numpy as np
import json
# 支持中文路径
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
# 支持中文属性表字段
gdal.SetConfigOption("SHAPE_ENCODING", "")

def writeRecShpFile(extentDictJson,outPath):
    """
    将字典形式的矩形范围写入Shp文件当中
    :param extentDictJson: 字典形式矩阵范围的Json文件，格式为{GridName:[左上经，左上纬，右下经，右下纬]}
    :param outPath: 输出shp路径
    :return: None
    """
    with open(extentDictJson,'r') as f:
        extentDict = json.load(f)
    ogr.RegisterAll()
    strDriverName = "ESRI Shapefile"
    oDriver = ogr.GetDriverByName(strDriverName)

    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
        return
    oDS = oDriver.CreateDataSource(outPath)
    if oDS == None:
        print("创建文件【%s】失败！", outPath)
        return
    # 创建WGS84坐标
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    oLayer = oDS.CreateLayer("GridRec",srs, ogr.wkbPolygon)
    if oLayer is None:
        print("图层创建失败！")
        return

    # oFieldID = ogr.FieldDefn("ID",ogr.OFTInteger)
    # oLayer.CreateField(oFieldID,1)
    oFieldName = ogr.FieldDefn('GridName',ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName,1)
    for i,(k,v) in enumerate(extentDict.items()):
        print('Writing %s'%(k))
        feature = ogr.Feature(oLayer.GetLayerDefn())
        # feature.SetField(0,i)
        feature.SetField(0,k)
        wkt = 'POLYGON((%f %f,%f %f,%f %f,%f %f,%f %f))'%(
            v[0],v[1],v[0],v[3],v[2],v[3],v[2],v[1],v[0],v[1]
        )
        geoRec = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(geoRec)
        oLayer.CreateFeature(feature)
        feature=None
    oDS.Destroy()
    print("shp文件生成完成!")

if __name__ == '__main__':
    extentJson = r'F:\Data\2.5TO10\数据说明及地理信息找回\AllSamplesGeoExtent.json'
    outShp = r'F:\Data\2.5TO10\SamplesShp\AllSamples.shp'
    writeRecShpFile(extentJson,outShp)


