#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
训练集生成
'''
from datetime import datetime
def read(path):
    fo = open(path)
    d = {}
    for line in fo:
        line = line.strip('\n')
        index = line.find(',')
        d[line[:index]] = line[(index + 1):]
    return d


# 加载特征字典
dict_user = read('feature/user_feature')
dict_merchant = read('feature/merchant_feature')
dict_coupon = read('feature/coupon_feature')

# 生成训练文件
raw_data = open('train_data/ccf_offline_stage1_train.csv')
train_data = open('corpus/train_data.txt', 'a')
next(raw_data)
for line in raw_data:
    line = line.strip('\n')
    params = line.split(',')
    if params[2] != 'null':
        new_line = dict_user.get(params[0], '0,0,0,0') + ',' + dict_merchant.get(params[1], '0,0,0,0') + ',' + dict_coupon.get(params[2], '0,0,0,0')
        if params[3] == 'null':
            feature_discount = '0,0,0'
        else:
            if params[3].find(':') == -1:
                feature_discount = params[3] + ',0,0'
            else:
                discounts = params[3].split(':')
                feature_discount = str(int(discounts[0]) / int(discounts[1])) + ',' + discounts[0] + ',' + discounts[1]

        new_line = new_line + ',' + feature_discount + ',' + ('-1' if params[4] == 'null' else params[4])
        if params[6] == 'null':
            label = 0
        else:
            a = datetime.strptime(params[5], '%Y%m%d')
            b = datetime.strptime(params[6], '%Y%m%d')
            if (b - a).days <= 15 :
                label = 1
            else:
                label = 0
        new_line = new_line + ',' + str(label) + '\n'
        train_data.write(new_line)

print('结束')