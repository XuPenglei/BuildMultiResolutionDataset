#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   datasetUtils.py
@Time    :   2020年4月16日15:36:10
@Author  :   Xu Penglei
@Version :   1.0
@Contact :   xupenglei87@163.com
@Desc    :   None
'''

import numpy as np
from glob import glob
from fnmatch import fnmatch
import os

def readTxt(txtPath):
    with open(txtPath,'r') as f:
        lines = f.readlines()
    LT = lines[3]
    RD = lines[5]
    def splitLine(line):
        line = line.split('：')[2]
        line = line.split(',')
        r = [float(r) for r in line]
        return r
    return splitLine(LT),splitLine(RD)

def readExtent(baseDir):
    # 读出每个格子的范围
    name_list = [n for n in os.listdir(baseDir) if fnmatch(n,'*.txt')]
    name_list = [n.replace('.txt','') for n in name_list]
    grid_name = name_list[0].split('_')[0]
    x_max = max([int(n.split('_')[1]) for n in name_list])+1
    y_max = max([int(n.split('_')[2]) for n in name_list])+1
    extent_arr = np.zeros((x_max,y_max,2,2))
    for x in range(x_max):
        for y in range(y_max):
            name = '_'.join([grid_name,str(x),str(y)])+'.txt'
            path = os.path.join(baseDir,name)
            LT,RD = readTxt(path)
            extent_arr[x,y,0,:] = np.array(LT)
            extent_arr[x,y,1,:] = np.array(RD)
    return extent_arr

def locateGrid(extent_arr,specific_extent):
    # specific_extent格式为[LT,RD]
    gridLT = extent_arr[0,0,0,:]
    gridRD = extent_arr[-1,-1,1,:]
    spe_LT = specific_extent[0]
    spe_RD = specific_extent[1]
    if spe_LT[0]<gridLT[0] or spe_LT[1]>gridLT[1]:
        print("左上角超出网格范围: GridLT",gridLT,'输入LT',spe_LT)
    if spe_RD[0]>gridRD[0] or spe_RD[1]<gridRD[1]:
        print("右下角超出网格范围: GridRD",gridRD,'输入RD',spe_RD)
    LT = [max(spe_LT[0],gridLT[0]),min(spe_LT[1],gridLT[1])]
    RD = [min(spe_RD[0],gridRD[0]),max(spe_RD[1],gridRD[1])]
    patch = searchPatch(extent_arr,(LT,RD))
    return patch

def searchPatch(extent_arr,extent):
    # 搜索在范围内的patch
    LT,RD = extent
    patch_LT = np.zeros([extent_arr.shape[0],extent_arr.shape[1]],dtype=np.byte) # 在LT右下方
    patch_RD = np.zeros([extent_arr.shape[0],extent_arr.shape[1]],dtype=np.byte) # 在RD左上方
    sum_LT=sum_RD=np.inf
    for x in range(extent_arr.shape[0]):
        for y in range(extent_arr.shape[1]):
            if pointInPatch(LT,extent_arr[x,y],'LT'):
                patch_LT_t = np.zeros_like(patch_LT)
                patch_LT_t[x:,y:]=1
                if np.sum(patch_LT_t)<sum_LT:
                    patch_LT=patch_LT_t
                    sum_LT=np.sum(patch_LT_t)
            if pointInPatch(RD,extent_arr[x,y],'RD'):
                patch_RD_t = np.zeros_like(patch_RD)
                patch_RD_t[:x+1,:y+1]=1
                if np.sum(patch_RD_t) < sum_RD:
                    patch_RD = patch_RD_t
                    sum_RD = np.sum(patch_RD_t)
    patch = np.logical_and(patch_LT,patch_RD)
    return np.where(patch==1)

def pointInPatch(point,patch,type):
#     判断点是否在范围内，type为LT或RD
    assert type in ['LT','RD']
    if type == 'LT':
        if patch[0][0]<=point[0]<patch[1][0] and patch[0][1]>=point[1]>patch[1][1]:
            return True
    else:
        if patch[0][0] < point[0] <= patch[1][0] and patch[0][1] > point[1] >= patch[1][1]:
            return True
    return False


if __name__ == '__main__':
    extentArr = readExtent(r'G:\jpg\IMG1\Level18')
    patch = locateGrid(extentArr,[[109.445800781,19.123077393],[110.216217041,18.159027100]])
    print(extentArr[patch])



