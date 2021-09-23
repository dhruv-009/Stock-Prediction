from sklearn.preprocessing import MinMaxScaler
import math
import numpy as np
from itertools import chain
import matplotlib.pyplot as plt
from io import StringIO

def merge(df, model):
    df = df.dropna(how='any')
    data = df.filter(['Close']).values
    test_data, scaler = scaledData(data)
    output = prediction(10, test_data, scaler, model)
    lst_final = convert_input(output)
    mx = findMax(lst_final)
    mn = findMin(lst_final)
    profit = maxProfit(mn, mx)
    final_profit = finalProfit(profit)
    return {"lst_final": lst_final, "mx": mx, "mn": mn, "profit": profit, "final_profit": final_profit,"output":output}


def scaledData(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    train_data_len = math.ceil(len(data) * 0.80)
    test_data = scaled_data[train_data_len - 110:, :]
    return (test_data[151:], scaler)


def prediction(num, test_data, scaler, model):
    x_input = test_data.reshape(1, -1)
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()
    lst_output = []
    n_steps = 110
    p = n_steps
    i = 0
    while(i < num):

        if(len(temp_input) > p):
            x_input = np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            lst_output.extend(yhat.tolist())
            i = i+1
        else:
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            #print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            #print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i = i+1
    output = scaler.inverse_transform(lst_output)
    return output


def convert_input(output):
    lst_tolist = output.tolist()
    lst_final = list(chain.from_iterable(lst_tolist))
    return lst_final


def findMin(arr):
    ans = []
    for i in range(len(arr)):
        if i == 0 or i == len(arr)-1:
            if i == 0 and arr[i] < arr[i+1]:
                ans.append((arr[i], i))
            if i == len(arr)-1 and arr[i-1] > arr[i]:
                ans.append((arr[i], i))
        else:
            if arr[i-1] > arr[i] and arr[i] < arr[i+1]:
                ans.append((arr[i], i))
    if ans == []:
        return [(0, 0)]
    return ans


def findMax(arr):
    ans = []
    for i in range(len(arr)):
        if i == 0 or i == len(arr)-1:
            if i == len(arr)-1 and arr[i-1] < arr[i]:
                ans.append((arr[i], i))
        else:
            if arr[i-1] < arr[i] and arr[i] > arr[i+1]:
                ans.append((arr[i], i))
    if ans == []:
        return [(0,0)]
    return ans


def maxProfit(mn, mx):
    profit = []
    for x, i in mn:
        for y, j in mx:
            if y-x > 0 and j > i:
                profit.append((i, j, y-x))
    if profit == []:
        return [(0,0,0)]
    return profit


def finalProfit(profit):
    mx = -1
    px, py, pro = 0, 0, 0
    for x, y, p in profit:
        if p >= mx:
            px, py, pro = x, y, p
            mx = p
    return (px, py, pro)




def return_graph(df,output):
    day_new = np.arange(1, 756)
    day_pred = np.arange(756, 756+10)
    fig  = plt.figure(figsize=(14, 6))

    plt.plot(day_new, df[['Close']])
    plt.plot(day_pred, output)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data
