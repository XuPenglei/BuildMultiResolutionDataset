#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   map2mask.py
@Time    :   2020/04/15 15:43:33
@Author  :   Xu Penglei 
@Version :   1.0
@Contact :   xupenglei87@163.com
@Desc    :   None
'''

# here put the import lib
import glob
import numpy as np
import multiprocessing.dummy as multiprocessing
from osgeo import gdal,ogr,gdal_array
import matplotlib.pyplot as plt


def colorAlign_singleBand(arr,value_list,mask):
    # 单波段的颜色查询
    idxArr_num = len(value_list)
    idx_list = []
    for i in range(idxArr_num):
        if mask:
            a = arr[mask[i]]
            idx = np.where(a==value_list[i])
            idx_list.append(np.array(mask[i]).squeeze()[idx])
        else:
            a = arr
            idx = np.where(a==value_list[i])
            idx_list.append(idx)        
    return idx_list
        
def Search(map_path,value_list=[251,251,250],type='tif'):
    # 查找对应颜色并转换成掩膜
    data = gdal.Open(map_path)
    im_w = data.RasterXSize
    im_h = data.RasterYSize
    im_bands = 3
    im_transform = data.GetGeoTransform()
    with open(map_path.replace('.'+type,'.prj')) as f:
        im_proj = f.read()
    # im_proj = data.GetProjection()
    mask_idx = None
    mask = np.zeros([im_h*im_w],dtype=np.byte)
    for b in range(im_bands):
        dt = data.GetRasterBand(b+1)
        mask_idx = colorAlign_singleBand(dt.ReadAsArray().reshape(-1),[value_list[b]],mask_idx)
    for m in mask_idx:
        mask[m]=1
    infor_dict = dict(proj = im_proj,transform = im_transform, w =im_w, h=im_h)
    return mask.reshape(im_h,im_w),infor_dict

def savetif(outpath,arr,info_dict,type='GTiff'):
    # 保存tif文件
    driver = gdal.GetDriverByName(type)
    new_raster = driver.Create(outpath,info_dict['w'],info_dict['h'],
                              1,gdal.GDT_Byte)
    new_raster.SetGeoTransform(info_dict['transform'])
    new_raster.SetProjection(info_dict['proj'])
    raster_band = new_raster.GetRasterBand(1)
    raster_band.WriteArray(arr)



if __name__ == "__main__":
    mask,info = Search(r'C:\Users\XuPenglei\Desktop\test\17-12-6\ditu\Level18\ditu.tif')
    savetif(r'C:\Users\XuPenglei\Desktop\test\17-12-6\ditu\mask.tif',mask,info)
    # plt.imshow(mask)
    # plt.show()
    



    