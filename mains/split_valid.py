# -*- coding: utf-8 -*-
"""
@ Time    : 2020/7/3 11:19
@ Author  : Xu Penglei
@ Email   : xupenglei87@163.com
@ File    : split_valid.py
@ Desc    : None
"""

from skimage.io import imread,imsave
from glob import glob
import os
import random
# ————————————————————————————————————————————————————from test data
# img_folder = r'F:\Data\ZT_SRDataset\四个定量精度评价区\IMG2p5'
# label_folder = 'F:\Data\ZT_SRDataset\四个定量精度评价区\GT2p5TF'
# out_img = r'F:\Data\test\NASUnetTest\K80val\img'
# out_label = r'F:\Data\test\NASUnetTest\K80val\label'
# imgs = glob(os.path.join(img_folder,'*.tif'))
# for i in imgs:
#     base_name = os.path.basename(i)
#     arr = imread(i)
#     label = imread(os.path.join(label_folder,base_name))
#     for row in range(3):
#         for col in range(5):
#             split_arr = arr[1000+row*256:1256+row*256,1000+col*256:1256+col*256]
#             split_label = label[1000+row*256:1256+row*256,1000+col*256:1256+col*256]
#             name = base_name.split('.')[0]
#             imsave(os.path.join(out_img,name+'_%d_%d.tif'%(row,col)),split_arr)
#             imsave(os.path.join(out_label, name + '_%d_%d.tif' % (row, col)), split_label)
# -------------------------------------------------------

"""img_folder = r'F:\Data\2.5TO10\BuildGT2p5WithoutSmallPatch_目视删除'
names = os.listdir(img_folder)
no_cloud = [n.split('.')[0] for n in names if 'cloud' not in n]
val_names = []
cityNames=['beijing','fuzhou','guangzhou',
               'guiyang','hangzhou','hefei',
               'jinan','kunming','nanchang',
               'nanjing','ningbo','shenzhen',
               'shijiazhuang','suzhou','tianjin',
               'xian','xiamen','zhengzhou']
names = [[n for n in no_cloud if c in n] for c in cityNames]
for c in names:
    val_names.extend(random.sample(c,20))
print(len(val_names))
# val_names = random.sample(no_cloud,300)
with open('val_new.txt','w') as f:
    f.write(','.join(val_names))"""


img_folder = r'F:\Data\2.5TO10\BuildGT2p5WithoutSmallPatch_目视删除'
names = os.listdir(img_folder)
no_cloud = [n.split('.')[0] for n in names if 'cloud' not in n]
test_names = random.sample(no_cloud,3000)
# val_names = random.sample(no_cloud,300)
with open('lr_test.txt','w') as f:
    f.write(','.join(test_names))





