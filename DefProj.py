#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DefProj.py
@Time    :   2020/04/15 15:12:57
@Author  :   Xu Penglei 
@Version :   1.0
@Contact :   xupenglei87@163.com
@Desc    :   None
'''

# here put the import lib
import arcpy
import os
from fnmatch import fnmatch

def defineProj(data_path):
    prj_path = data_path.replace('.jpg','.prj')
    prj = arcpy.SpatialReference(prj_path)
    arcpy.DefineProjection_management(data_path,prj)
    print data_path+' finished!'

if __name__ == "__main__":
    name = r'G:\jpg\IMG17\Level18'
    fn_list = [n for n in os.listdir(name) if fnmatch(n,'*.jpg')]
    dir_list = [os.path.join(name,fn) for fn in fn_list]
    for n in dir_list:
        defineProj(n)
    