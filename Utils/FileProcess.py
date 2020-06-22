# -*- coding: utf-8 -*-
"""
@ Time    : 2020/6/22 8:45
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : FileProcess.py
@ Desc    : 本文件中均为文件操作相关函数
"""

from glob import glob
from tqdm import tqdm
import os
import shutil

def RemoveReat(fileDir):
    """
    删除文件夹中文件名中有(n)的重复文件
    :param fileDir: 待筛选的文件夹
    :return:
    """
    Flist = os.listdir(fileDir)
    unique_list = [f for f in Flist if '(' not in f and ')' not in f]
    del_n = 0
    unique_with_symble= []
    for file in tqdm(Flist):
        if '(' in file or ')' in file:
            n_t = file.replace(file[file.index('('):(file.index(')')+1)],'')
            if n_t in unique_list:
                os.remove(os.path.join(fileDir,file))
                del_n+=1
            else:
                unique_with_symble.append(n_t)
    print('%d files in dir, delete %d repeat files, left %d files'%(
        len(Flist),del_n, len(unique_list)
    ))
    print(unique_with_symble)

if __name__ == '__main__':
    fileDir = r'F:\Data\2.5TO10\Image10m_png'
    RemoveReat(fileDir)
