import pandas as pd
import math

_df = pd.read_csv('model/data.csv')
df = _df.drop(labels=['other', 'source'], axis=1)
# df.prev_crops.fillna('', inplace=True)
# df = df.soil_types.fillna('', inplace=True)
w_ = {'temp': 3, 'rainfall': 2, 'soil_types': 2, 'ph': 1, 'prev_crops': 3}


def check_float(s):
    try:
        x = float(s)
        if math.isnan(x):
            return False
        return True
    except ValueError:
        return False
    return False


def gbell(x, l, h):
    if not check_float(x):
        return 0
    a = float(h)-float(l)  # 2*(h-l)/3
    b = 3  # (h+l)/(h-l)
    c = (float(h)+float(l))/2
    # a = length of the curve
    # b = used to describe the slope of the curve
    # c = center of the curve on x-axis
    # constructing a generalized bell curve
    # output: [-1, 1]
    # ref: https://functionbay.com/documentation/onlinehelp/default.htm#!Documents/fuzzymembershipfunctions.htm
    # simulator: https://www.desmos.com/calculator/3iioyvma2l
    return 1/(1+pow(abs((float(x)-c)/a), 2*b))


def get_scores_dict(row, inp_):
    res = {'temp': 0, 'rainfall': 0, 'ph': 0, 'soil': 0, 'prev_crops': 0}
    score = 0
    max_score = 0

    if 'temp' in inp_:
        res['temp'] = gbell(inp_['temp'], row['min_temp_c'], row['max_temp_c'])*w_['temp']
    score = score + res['temp']
    max_score = max_score + 1

    if 'rainfall' in inp_:
        res['rainfall'] = gbell(inp_['rainfall'], row['min_rainfall_mm'], row['max_rainfall_mm'])*w_['rainfall']
    score = score + res['rainfall']
    max_score = max_score + 1

    if 'ph' in inp_:
        if not math.isnan(row['min_ph']) and not math.isnan(row['max_ph']):
            res['ph'] = gbell(inp_['ph'], row['min_ph'], row['max_ph'])*w_['ph']
    score = score + res['ph']
    max_score = max_score + 1

    # for uniqueness of soil type. the limited the number of soil types, the more imporant the feature
    _soils_arr = row['soil_types'].split(",")
    if 'soil_types' in inp_:
        if inp_['soil_types'] in _soils_arr:
            res['soil'] = res['soil'] + (1/len(_soils_arr))*w_['soil_types']
    score = score + res['soil']
    max_score = max_score + 1/len(_soils_arr)

    # for uniqueness of previous crops. the limited the number of previous crops, the more imporant the feature
    _prev_crops = str(row['prev_crops']).split(",")
    if 'prev_crops' in inp_:
        if inp_['prev_crops'] in _prev_crops:
            res['prev_crops'] = res['prev_crops'] + (1/len(_prev_crops))*w_['prev_crops']
    score = score + res['prev_crops']
    max_score = max_score + 1/len(_prev_crops)

    res['total'] = score
    return res


def get_all_scores(inp_):
    out_ = {}
    for i, row in df.iterrows():
        out_[row['plant']] = get_scores_dict(row, inp_)
    return out_
