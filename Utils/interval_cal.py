#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 22:13
# @Author  : XuPenglei
# @Site    : 
# @File    : interval_cal.py
# @Software: PyCharm
# @email  : xupenglei87@163.com
# @Description: 进行区间运算

import math

def intersect(inter1,inter2):
    """
    两区间的交集
    :param inter1: 第一区间，形式为[left,right], 主区间
    :param inter2: 第二区间，形式为[left,right]
    :return: 交集或者空集
    """
    l = max(inter1[0],inter2[0])
    r = min(inter1[1],inter2[1])
    if l<r:
        if l==inter1[0] and r == inter1[1]:
            return [l,r],2
        else:
            return [l,r],1
    else:
        return None,0

def diff(inter_main,inter_aux):
    """
    计算两区间的差
    :param inter_main: 主要区间
    :param inter_aux: 辅助区间,是在主要区间上的子集
    :return: inter_main-inter_aux
    """

    if inter_main[0] == inter_aux[0] and inter_main[1] == inter_aux[1]:
        return None
    if inter_main[0] < inter_aux[0] and inter_main[1] > inter_aux[1]:
        return [[inter_main[0],inter_aux[0]],[inter_aux[1],inter_main[1]]]
    if inter_main[0]==inter_aux[0]:
        l = inter_aux[1]
    else:
        r = inter_aux[0]
    if inter_aux[1]==inter_main[1]:
        l = inter_main[0]
    else:
        r = inter_main[1]
    if l < r:
        return [[l, r]]
    else:
        return None


if __name__ == '__main__':
    a=[3,5]
    b=[4,5]
    print(diff(b,a))