#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
特征处理
'''
def write(dict_user, feature_name):
    fo = open('feature/' + feature_name, 'a')
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
#用户特征
dict_user = {}
#商户特征
dict_merchant_visit = {}
dict_merchant_buy = {}
dict_merchant = {}
#消费券特征
dict_coupon_visit = {}
dict_coupon_buy = {}
dict_coupon = {}

for line in train_data:
    line = line.strip('\n')
    params = line.split(',')
    user_feature = parser(params)
    if params[0] in dict_user:
        dict_user[params[0]] = list(map(lambda a, b: a + b, dict_user[params[0]], user_feature))
    else:
        dict_user[params[0]] = user_feature


    if params[1] in dict_merchant_visit:
        dict_merchant_visit[params[1]].append(params[0])
    else:
        dict_merchant_visit[params[1]] = [params[0]]

    if params[1] in dict_merchant_buy:
        if params[6] != 'null':
            dict_merchant_buy[params[1]].append(params[0])
    else:
        if params[6] != 'null':
            dict_merchant_buy[params[1]] = [params[0]]
        else:
            dict_merchant_buy[params[1]] = []

    if params[2] in dict_coupon_visit:
        dict_coupon_visit[params[2]].append(params[0])
    else:
        dict_coupon_visit[params[2]] = [params[0]]

    if params[2] in dict_coupon_buy:
        if params[6] != 'null':
            dict_coupon_buy[params[2]].append(params[0])
    else:
        if params[6] != 'null':
            dict_coupon_buy[params[2]] = [params[0]]
        else:
            dict_coupon_buy[params[2]] = []

for k in dict_merchant_visit.keys():
    features = [0] * 4
    visit_list = dict_merchant_visit[k]
    buy_list = dict_merchant_buy[k]
    features[0] = len(set(visit_list))
    features[1] = len(visit_list)
    features[2] = len(set(buy_list))
    features[3] = len(buy_list)
    dict_merchant[k] = features

for k in dict_coupon_visit.keys():
    features = [0] * 4
    visit_list = dict_coupon_visit[k]
    buy_list = dict_coupon_buy[k]
    features[0] = len(set(visit_list))
    features[1] = len(visit_list)
    features[2] = len(set(buy_list))
    features[3] = len(buy_list)
    dict_coupon[k] = features

# write(dict_user, 'user_feature')
    
# write(dict_merchant, 'merchant_feature')

write(dict_coupon, 'coupon_feature')
