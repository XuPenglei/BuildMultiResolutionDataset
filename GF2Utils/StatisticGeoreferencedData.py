#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/27 20:49
# @Author  : XuPenglei
# @Site    : 
# @File    : StatisticGeoreferencedData.py
# @Software: PyCharm
# @email  : xupenglei87@163.com
# @Description: 统计已经配准好的高分二号的信息

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
from glob import glob
from tqdm import tqdm
# 支持中文路径
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
# 支持中文属性表字段
gdal.SetConfigOption("SHAPE_ENCODING", "")

def writeJson(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)
    print('Write Json Successfully!')

mother_dir=r''
dict = {}
for d in tqdm(os.listdir(mother_dir)):
    son_dir = os.path.join(mother_dir,d)
    img_path = glob(os.path.join(son_dir,'*FUSION.tif'))[0]
    data = gdal.Open(img_path)
    dict[d]=data.GetProjection()
writeJson(dict,'GeoReferencedProjection.json')

