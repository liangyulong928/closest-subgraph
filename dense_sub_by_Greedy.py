import pandas as pd
import numpy as np
import math


def readData():
    data = pd.read_csv('data/email-EU.edges',sep=" ",header=None)
    return data

def init(data):
    array_list = []
    array_list.append(np.array(data[0]))
    array_list.append(np.array(data[1]))
    array_list = np.array(array_list)
    array_length = [[min(array_list[0]),min(array_list[1])],[max(array_list[0]),max(array_list[1])]]
    return array_length,array_list.T

def checkMinCount(array_length,array_list):
    count_list = []
    count_list.append(np.sum(array_list.T[0]==array_length[0][0])/(array_length[1][0] - array_length[0][0] + 1))
    count_list.append(np.sum(array_list.T[0]==array_length[1][0])/(array_length[1][0] - array_length[0][0] + 1))
    count_list.append(np.sum(array_list.T[1]==array_length[0][1])/(array_length[1][1] - array_length[0][1] + 1))
    count_list.append(np.sum(array_list.T[1]==array_length[1][1])/(array_length[1][1] - array_length[0][1] + 1))
    # print(count_list)
    index = count_list.index(min(count_list))
    if(index==0):
        return index,np.sum(array_list.T[0]==array_length[0][0])
    elif(index==1):
        return index,np.sum(array_list.T[0]==array_length[1][0])
    elif(index==2):
        return index,np.sum(array_list.T[1]==array_length[0][1])
    else:
        return index,np.sum(array_list.T[1]==array_length[1][1])
    

def slice_cut(index,count,array_length,array_list):
    if(index==0):
        # print(f"对x轴左侧进行切片,切片坐标：x = {array_length[0][0]}")
        for i in range(count):
            index_key = np.where(array_list.T[0]==array_length[0][0])[0][0]
            array_list = np.delete(array_list,index_key,0)
        array_length[0][0] = min(array_list.T[0])
    if(index==1):
        # print(f"对x轴右侧进行切片,切片坐标：x = {array_length[1][0]}")
        for i in range(count):
            index_key = np.where(array_list.T[0]==array_length[1][0])[0][0]
            array_list = np.delete(array_list,index_key,0)
        array_length[1][0] = max(array_list.T[0])
    if(index==2):
        # print(f"对y轴下侧进行切片,切片坐标：y = {array_length[0][1]}")
        for i in range(count):
            index_key = np.where(array_list.T[1]==array_length[0][1])[0][0]
            array_list = np.delete(array_list,index_key,0)
        array_length[0][1] = min(array_list.T[1])
    if(index==3):
        # print(f"对y轴上侧进行切片,切片坐标：y = {array_length[1][1]}")
        for i in range(count):
            index_key = np.where(array_list.T[1]==array_length[1][1])[0][0]
            array_list = np.delete(array_list,index_key,0)
        array_length[1][1] = max(array_list.T[1])
    return array_length,array_list

def calculate_density(array_length,array_list):
    density = len(array_list) / math.sqrt((array_length[1][1] - array_length[0][1] + 1)*(array_length[1][0] - array_length[0][0] + 1))
    return density

data = readData()
array_length,array_list = init(data)
density = 0
while(len(array_list) > 1):
# for i in range(20):
    # print("-"*20)
    # print("进行切片：")
    index,count = checkMinCount(array_length,array_list)
    array_length,array_list = slice_cut(index,count,array_length,array_list)
    if(density < calculate_density(array_length,array_list)):
        density = calculate_density(array_length,array_list)
        array_count = array_length
        print(f"更新密度为：{density}，密度区间为{array_count}")
    