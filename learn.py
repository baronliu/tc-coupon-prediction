#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
模型计算
'''
import numpy as np
import sklearn
from sklearn import svm

def show_accuracy(x, y):
    a,b,c = 0,0,0
    for idx,item in enumerate(x):
        if item == 1:
            a += 1
            if item == y[idx]:
                c += 1
        if y[idx] == 1:
            b += 1
    print('准确率为：' + str(c / b))
    print('查全率为：' + str(c / a))
        

data = np.loadtxt('corpus/train_data.txt', 'float', '#', ',')
x, y = np.split(data, (-1,), axis=1)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, random_state=1, train_size=0.6)

clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr').fit(x_train, y_train.ravel())
y_test_result = clf.predict(x_test)
show_accuracy(y_test, y_test_result)
