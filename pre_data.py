#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
特征处理
'''
def write(dict_user):
    fo = open('feature/user_feature', 'a')
    fo.truncate()
    for k, features in dict_user.items():
        fo.write(k + ',' + ','.join(str(v) for v in features) + '\n')
    fo.close()


def parser(params):
    user_feature = [0] * 4
    user_feature[0] = 1
    if params[6] != 'null':
        if params[2] != 'null':
            # 有优惠券购买了商品
            user_feature[1] = 1
        else:
            # 没有优惠券购买了商品
            user_feature[2] = 1
    else:
        if params[2] != 'null':
            # 有优惠券没购买商品
            user_feature[3] = 1
    return user_feature

train_data = open('train_data/ccf_offline_stage1_train.csv')
next(train_data)

dict_user = {}
dict_merchant = {}

for line in train_data:
    line = line.strip('\n')
    params = line.split(',')
    user_feature = parser(params)
    if params[0] in dict_user:
        dict_user[params[0]] = list(map(lambda a, b: a + b, dict_user[params[0]], user_feature))
    else:
        dict_user[params[0]] = user_feature
write(dict_user)
    
