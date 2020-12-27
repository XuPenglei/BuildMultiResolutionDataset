# -*- coding: utf-8 -*-
"""
@ Time    : 2020/8/1 15:11
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : GenerateSampleLabel.py
@ Desc    : 通过样本的范围与全景标签裁剪出样本对应的标签图
"""

from osgeo import gdal,ogr
import skimage.io as io
import numpy as np
from Utils.RasterProcess import RasterProcessor
import json
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def clipGT(cityName,GT_dir,extentJson,outdir,HR):
    print(cityName)
    p = RasterProcessor()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # whoIMG = r'F:\Data\trainSHP\tempt\TFguangzhou.tif'
    whoIMG = os.path.join(GT_dir,'TF'+cityName+'.tif')
    data = gdal.Open(whoIMG)
    geomat = data.GetGeoTransform()
    proj = data.GetProjection()
    raster = io.imread(whoIMG)
    # extentJson = r'F:\Data\2.5TO10\数据说明及地理信息找回\AllSamplesGeoExtent.json'

    # outdir = r'F:\Data\2.5TO10\BuildGT2P5_New'
    with open(extentJson,'r') as f:
        samplesExtent = json.load(f)
    city_dict = {}
    for k,v in samplesExtent.items():
        if cityName in k:
            city_dict.update({k:v})
    for k,v in tqdm(city_dict.items()):
        samples_geomat = list(geomat)
        samples_geomat[0],samples_geomat[3]=v[0],v[1]
        samples = p.clipWithGeo(raster,v[:2],v[2:],geomat)
        if HR:
            samples_resize,new_geomat = p.resampleWithGeo(samples,tuple(samples_geomat),256,256)
        else:
            samples_resize, new_geomat = p.resampleWithGeo(samples, tuple(samples_geomat), 64, 64)
        if 'cloud' in k and HR:
            io.imsave(os.path.join(outdir, k + '_HR.tif'), samples_resize)
            temp_data = gdal.Open(os.path.join(outdir, k + '_HR.tif'), gdal.GA_Update)
        else:
            io.imsave(os.path.join(outdir,k+'.tif'),samples_resize)
            temp_data =gdal.Open(os.path.join(outdir,k+'.tif'),gdal.GA_Update)
        temp_data.SetGeoTransform(new_geomat)
        temp_data.SetProjection(proj)
        del temp_data

def showLabel(gt1dir,gt2dir,imgdir,name,img_format = 'tif'):
    fig,ax = plt.subplots(1,3,figsize=(12,5))
    if 'cloud' in name:
        t_name=name.replace('.','_HR.')
        gt1 = io.imread(os.path.join(gt1dir, name).replace(img_format, 'png'))
    else:
        gt1 = io.imread(os.path.join(gt1dir,name).replace(img_format,'png'))
    ax[0].imshow(gt1,cmap='gray')
    ax[0].set_title('Origin')
    gt2 = io.imread(os.path.join(gt2dir,name).replace(img_format,'tif'))
    ax[1].imshow(gt2,cmap='gray')
    ax[1].set_title('New')
    if name.split('.')[-1] == 'npy':
        img= np.load(os.path.join(imgdir,name))[:,:,:3]
    else:
        img = io.imread(os.path.join(imgdir,name))
    ax[2].imshow(img)
    ax[2].set_title(name)
    plt.show()


if __name__ == '__main__':
    cityNames=['beijing','fuzhou','guangzhou',
               'guiyang','hangzhou','hefei',
               'jinan','kunming','nanchang',
               'nanjing','ningbo','shenzhen',
               'shijiazhuang','suzhou','tianjin',
               'xian','xiamen','zhengzhou']
    GTdir=r'F:\Data\trainSHP\GT2P5_'
    outdir=r'F:\Data\2.5TO10\BuildGT10m_New'
    extentJson = r'F:\Data\2.5TO10\数据说明及地理信息找回\AllSamplesGeoExtent.json'
    for city in cityNames:
        clipGT(city,GTdir,extentJson,outdir,HR=False)

    # oriDir = r'F:\Data\2.5TO10\BuildGT2p5'
    # newDir = r'F:\Data\2.5TO10\BuildGT2P5_New'
    # # IMGdir = r'F:\Data\2.5TO10\Image91_256_tif'
    # IMGdir = r'F:\Data\2.5TO10\Image10m_png'
    # for i in os.listdir(IMGdir):
    #     if 'cloud' in i:
    #         continue
    #     name = os.path.basename(i)
    #     showLabel(oriDir,newDir,IMGdir,name,img_format='png')