#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 9:59
# @Author  : XuPenglei
# @Site    : 
# @File    : Searcher.py
# @Software: PyCharm
# @email  : xupenglei87@163.com
# @Description: 通过遍历的方式搜索网格，求取交集和差集

from Utils.interval_cal import *
import os
import math
from tqdm import tqdm

def remove_repeat(input_list):
    new_list = []
    if len(input_list)==0:
        return new_list
    for i in input_list:
        if i not in new_list:
            new_list.append(i)
    return new_list

class searcher():
    def __init__(self,extent,grids):
        self.lat_inter = extent[0]
        self.lng_inter = extent[1]
        self.grids = grids

    def inter_cal_2D(self,main_lat,main_lng,grid_lat,grid_lng):
        """
        计算2D网格的交和差
        :return:
        """
        intersect_lat,flag_lat = intersect(main_lat,grid_lat)
        intersect_lng, flag_lng = intersect(main_lng, grid_lng)
        if flag_lat*flag_lng!=0:
            diff_lat = diff(main_lat, intersect_lat)
            diff_lng = diff(main_lng, intersect_lng)
        if flag_lat*flag_lng==0:
            return None,None
        elif flag_lat==2 and flag_lng==2:
            return [main_lat,main_lng],None
        elif flag_lat==1 and flag_lng==1:
            intersect_ = [intersect_lat,intersect_lng]
            # diff_ = [[diff_lat,diff_lng],
            #          [diff_lat,intersect_lng],
            #          [intersect_lat,diff_lng]]
            diff_ = []
            diff_.extend([[dlat,dlng] for dlat in diff_lat for dlng in diff_lng])
            diff_.extend([[dlat,intersect_lng] for dlat in diff_lat])
            diff_.extend([[intersect_lat,dlng] for dlng in diff_lng])
            return intersect_,diff_
        elif flag_lat==1 and flag_lng==2:
            intersect_ = [intersect_lat,intersect_lng]
            diff_ = [[d,intersect_lng] for d in diff_lat]
            return intersect_,diff_
        elif flag_lat==2 and flag_lng==1:
            intersect_ = [intersect_lat,intersect_lng]
            diff_ = [[intersect_lat,d] for d in diff_lng]
            return intersect_,diff_

    def search_in_grids(self,lat_inter,lng_inter):
        """
        在所有网格中寻找目标的交区间和补区间
        :return:
        """

        # 交区间的集合
        inter_set = []
        # 交区间所在格子的集合
        grid_set = []
        # 待查询区间
        diff_set = []
        for g in tqdm(self.grids):
            grid_lat = g[0]
            grid_lng = g[1]
            inter_,diff_ = self.inter_cal_2D(lat_inter,lng_inter,grid_lat,grid_lng)
            if inter_ is None:
                continue
            else:
                inter_set.append(inter_)
                grid_set.append(g)
                if diff_ is not None:
                    new_diff = [n for n in diff_ if n not in diff_set]
                    diff_set.extend(new_diff)
        for i in inter_set:
            if i in diff_set:
                diff_set.remove(i)
        return remove_repeat(inter_set),remove_repeat(grid_set),remove_repeat(diff_set)

    def search_all(self):
        """搜索单个patch在所有网格上的位置"""
        inter_set,grid_set,diff_set = self.search_in_grids(self.lat_inter,self.lng_inter)
        # 无效集合，找不到
        invalid_set=[]
        while len(diff_set)!=0:
            new_diff_set=[]
            for d in diff_set:
                i_s,g_s,d_s = self.search_in_grids(d[0],d[1])
                if len(i_s)==0:
                    invalid_set.append(d)
                    continue
                inter_set.extend(i_s)
                grid_set.extend(g_s)
                new_diff_set.extend(d_s)
            diff_set=new_diff_set
        return map(remove_repeat,[inter_set,grid_set,invalid_set])

if __name__ == '__main__':
    grids = [[[0,3],[0,3]],
             [[3,5],[0,3]],
             [[3,5],[3,5]],
             [[0,3],[3,5]]
             ]
    extent = [[4,6],[4,6]]
    s = searcher(extent,grids)
    inter_set,grid_set,invalid_set = s.search_all()
    print(inter_set)
    print(grid_set)
    print(invalid_set)








