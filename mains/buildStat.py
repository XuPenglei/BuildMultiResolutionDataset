# -*- coding: utf-8 -*-
"""
@ Time    : 2020/8/14 9:59
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : buildStat.py
@ Desc    : 统计建筑物比例
"""

import skimage.io as io
import os
import numpy as np
from glob import glob
from tqdm import tqdm
import math
import shutil


def stat(dir,filenameJson=None):
    files = glob(os.path.join(dir,'*.tif'))
    build_dict = dict([[0,0],[1,0],[2,0],[3,0],[4,0],
                       [5,0],[6,0],[7,0],[8,0],[9,0],[10,0]])
    empty_img = []
    if filenameJson:
        with open(filenameJson,'r') as f:
            names = f.readlines()[0].replace('\n','')
        names = names.split(',')
        files = [os.path.join(dir,n+'.tif') for n in names]
    for f in tqdm(files):
        img = io.imread(f).reshape((-1))
        build = (img>1).sum()/len(img)
        if build==0:
            build_dict[0]+=1
            empty_img.append(f)
        else:
            build_dict[math.ceil(build*10)+1]+=1
    with open('empty.txt','w') as f:
        f.write(','.join(empty_img))
    with open('val_new.txt','r') as f:
        names = f.read()
        names = names.split(',')
        names = [os.path.join(dir,n+'.tif') for n in names]
        for n in names:
            if n in empty_img:
                print(n)
    return build_dict

def dealWithEmpty(emptytxt,valtxt,input_dir):
    with open(emptytxt,'r') as f:
        emptyImg = f.read().split(',')
        emptyImg = [os.path.basename(n) for n in emptyImg]
        emptyImg = [os.path.join(input_dir,n) for n in emptyImg]
    with open(valtxt,'r') as f:
        valIMG = f.read().split(',')
    newval=[]
    for n in emptyImg:
        shutil.move(n,r'F:\Data\2.5TO10\EmptyGT')
    # for n in valIMG:
    #     pat = os.path.join(r'F:\Data\2.5TO10\BuildGT2P5_New',n+'.tif')
    #     if pat not in emptyImg:
    #         newval.append(n)
    #     else:
    #         print(n)
    # with open('val_without_empty.txt','w') as f:
    #     f.write(','.join(newval))

if __name__ == '__main__':
    img_dir = r'F:\Data\2.5TO10\BuildGT10m_New'
    # text = r'E:\Projects\Unets\val_new.txt'
    # print(stat(img_dir))
    dealWithEmpty(r'E:\Projects\BuildMultiResolutionDataset\mains\empty.txt',
                  r'E:\Projects\BuildMultiResolutionDataset\mains\val_new.txt',
                  input_dir=img_dir)
