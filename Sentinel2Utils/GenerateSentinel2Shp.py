# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/19 11:58
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : GenerateGF2Shp.py
@ Desc    : 由统计的Sentinel2数据情况成成覆盖区域的shp文件
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

def writeRecShpFile(GF2Json, outPath, EPSG=4326):
    """
    将字典形式的矩形范围写入Shp文件当中
    :param GF2Json: 字典形式矩阵范围的Json文件，格式为{GridName:[左上经，左上纬，右下经，右下纬]}
    :param outPath: 输出shp路径
    :return: None
    """
    with open(GF2Json, 'r') as f:
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
    srs.ImportFromEPSG(EPSG)
    oLayer = oDS.CreateLayer("GridRec",srs, ogr.wkbPolygon)
    if oLayer is None:
        print("图层创建失败！")
        return

    # oFieldID = ogr.FieldDefn("ID",ogr.OFTInteger)
    # oLayer.CreateField(oFieldID,1)
    oFieldName = ogr.FieldDefn('GridName',ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName,1)
    for c,(k,v) in enumerate(extentDict.items()):
        for i,j in enumerate(v):
            print('Writing %s %d'%(k,i+1))
            extent = j['WGSExtent']
            feature = ogr.Feature(oLayer.GetLayerDefn())
            # feature.SetField(0,i)
            feature.SetField(0,k+str(i+1))
            wkt = 'POLYGON((%f %f,%f %f,%f %f,%f %f,%f %f))'%(
                extent[0],extent[1],extent[0],extent[3],
                extent[2],extent[3],extent[2],extent[1],extent[0],extent[1]
            )
            geoRec = ogr.CreateGeometryFromWkt(wkt)
            feature.SetGeometry(geoRec)
            oLayer.CreateFeature(feature)
            feature=None
    oDS.Destroy()
    print("%d 个城市已被统计！"%(c+1))
    print("shp文件生成完成!")

if __name__ == '__main__':
    Sentinel2Json = r'E:\Projects\BuildMultiResolutionDataset\Sentinel2Utils\Sentinel2WholeIMGInfo.json'
    outPath = r'E:\Projects\BuildMultiResolutionDataset\Sentinel2Utils\Sentinel2Shp\Sentinel2Extent.shp'
    writeRecShpFile(Sentinel2Json,outPath)
