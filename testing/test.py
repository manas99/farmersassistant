import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

w_ = {'temp': 3, 'rainfall': 2, 'soil_types': 2, 'ph': 1, 'prev_crops': 3}


def gbell(x, l, h):
    a = h-l  # 2*(h-l)/3
    b = 3  # (h+l)/(h-l)
    c = (h+l)/2
    # a = length of the curve
    # b = used to describe the slope of the curve
    # c = center of the curve on x-axis
    # constructing a generalized bell curve
    # output: [-1, 1]
    # ref: https://functionbay.com/documentation/onlinehelp/default.htm#!Documents/fuzzymembershipfunctions.htm
    # simulator: https://www.desmos.com/calculator/3iioyvma2l
    return 1/(1+pow(abs((x-c)/a), 2*b))


_df = pd.read_csv('data1.csv')
df = _df.drop(labels=['other', 'source'], axis=1)
# df.prev_crops.fillna('', inplace=True)
# df = df.soil_types.fillna('', inplace=True)


def get_scores_dict(row, inp_):
    res = {}
    score = 0
    max_score = 0

    res['temp'] = gbell(inp_['temp'], row['min_temp_c'], row['max_temp_c'])*w_['temp']
    score = score + res['temp']
    max_score = max_score + 1

    res['rainfall'] = gbell(inp_['rainfall'], row['min_rainfall_mm'], row['max_rainfall_mm'])*w_['rainfall']
    score = score + res['rainfall']
    max_score = max_score + 1

    res['ph'] = 0
    if not math.isnan(row['min_ph']) and not math.isnan(row['max_ph']):
        res['ph'] = gbell(inp_['ph'], row['min_ph'], row['max_ph'])*w_['ph']
        score = score + res['ph']
        max_score = max_score + 1

    # for uniqueness of soil type. the limited the number of soil types, the more imporant the feature
    _soils_arr = row['soil_types'].split(",")
    res['soil'] = 0
    for x in inp_['soil_type']:
        if x in _soils_arr:
            res['soil'] = res['soil'] + (1/len(_soils_arr))*w_['soil_types']
    score = score + res['soil']
    max_score = max_score + 1/len(_soils_arr)

    # for uniqueness of previous crops. the limited the number of previous crops, the more imporant the feature
    _prev_crops = str(row['prev_crops']).split(",")
    res['prev_crop'] = 0
    for x in inp_['prev_crop']:
        if x in _prev_crops:
            res['prev_crop'] = res['prev_crop'] + (1/len(_prev_crops))*w_['prev_crops']
    score = score + res['prev_crops']
    max_score = max_score + 1/len(_prev_crops)

    res['total'] = score
    return res


if __name__ == '__main__':
    inp_ = {'temp': 20, 'rainfall': 700, 'ph': 6, 'soil_type': ['loam'], 'prev_crop': []}

    out_ = {}
    for i, row in df.iterrows():
        out_[row['plant']] = get_scores_dict(row, inp_)

    labels = []
    tot_scores = []
    temp_scores = []
    rain_scores = []
    ph_scores = []
    soil_scores = []
    prev_scores = []

    for x in out_:
        labels.append(x)
        tot_scores.append(out_[x]['total'])
        temp_scores.append(out_[x]['temp'])
        rain_scores.append(out_[x]['rainfall'])
        ph_scores.append(out_[x]['ph'])
        soil_scores.append(out_[x]['soil'])
        prev_scores.append(out_[x]['prev_crops'])
        print(x+": ", out_[x])

    # plotting the graph
    index = np.arange(len(labels))

    plt.rcParams.update({'font.size': 5})
    plt.subplot(2, 3, 1)
    plt.bar(index, tot_scores)
    plt.ylabel('Total Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)

    plt.subplot(2, 3, 2)
    plt.bar(index, temp_scores)
    plt.ylabel('Temperature Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)

    plt.subplot(2, 3, 3)
    plt.bar(index, rain_scores)
    plt.ylabel('Rainfall Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)

    plt.subplot(2, 3, 4)
    plt.bar(index, ph_scores)
    plt.ylabel('pH Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)

    plt.subplot(2, 3, 5)
    plt.bar(index, soil_scores)
    plt.ylabel('Soil Type Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)

    plt.subplot(2, 3, 6)
    plt.bar(index, prev_scores)
    plt.ylabel('Previous Crop Scores', fontsize=10)
    plt.xticks(index, labels, rotation=30)
    plt.show()
