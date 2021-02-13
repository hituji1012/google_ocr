from google_ocr_lib import render_doc_text
# from google_ocr_api import render_doc_text

import numpy as np
import math
import pandas as pd

def rect_to_point(rect):
    """ 文字rectの中心座標 """
    x = []
    y = []
    for d in rect:
        if 'x' in d:
            x.append(d['x'])
        if 'y' in d:
            y.append(d['y'])
    return sum(x)/len(x), sum(y)/len(y)

def rect_ave_height_degree(data_list):
    """ 平均高さ、傾き """
    height = []
    degree = []
    for rect in data_list:
        x = []
        y = []
        for d in rect[0]:
            if 'x' in d:
                x.append(d['x'])
            if 'y' in d:
                y.append(d['y'])
        # データ不足しているのは無視します。
        if len(x)==4 and len(y)==4:
            height.append(((y[3]-y[0])+(y[2]-y[1]))/2)
            if (x[1]-x[0]) == 0:
                tan = 0
            else:
                tan = (y[1] - y[0]) / (x[1] - x[0])
            atan = np.arctan(tan) * 180 / math.pi
            degree.append(atan)
    # 平均値を返す。場合によっては中央値でもよい。
    return sum(height)/len(height), sum(degree)/len(degree)


# print(data_list)
def join_nearest(data_list, height):
    """ 近接の文字結合 """
    ret_data = []
    data_list.reverse()
    # データなくなるまで
    while data_list:
        d = data_list.pop()
        most_near = 0

        # 近接文字なくなるまで
        while most_near!=-1:
            rect = d[0]
            most_near = -1
            if ('x' in rect[1]) and ('y' in rect[1]):
                curent_x = rect[1]['x']
                curent_y = rect[1]['y']

                # 右に文字高さの 1/2 以内の近さがあれば
                temp_data = data_list.copy()
                for ind2, d2 in enumerate(temp_data):
                    rect2 = d2[0]
                    if ('x' in rect2[0]) and ('y' in rect2[0]):
                        other_x = rect2[0]['x']
                        other_y = rect2[0]['y']
                        # 距離の近いところ
                        if (abs(other_x-curent_x)<height/2) and (abs(other_y-curent_y)<height/2):
                            most_near = ind2
                            break

            # 文字連結
            if most_near>0:
                # 連結
                new_rect = []
                new_rect.append(rect[0])
                new_rect.append(rect2[1])
                new_rect.append(rect2[2])
                new_rect.append(rect[3])
                new_str = d[1] + d2[1]
                d = [new_rect, new_str]
                # 連結したデータも削除
                del data_list[ind2]
            else:
                ret_data.append(d)
                break

    return ret_data


if __name__ == '__main__':
    # OCR検知
    data_list = render_doc_text('sample.png')

    # 高さ、角度
    height, degree = rect_ave_height_degree(data_list)

    # 近接文字結合
    data_list = join_nearest(data_list, height)

    # 中央座標に変換して、DataFrameに変更
    new_data_list = []
    for d in data_list:
        x, y = rect_to_point(d[0])
        new_data_list.append([x, y, d[1]])
    df = pd.DataFrame(data=new_data_list, columns=['x', 'y', 'text'])

    print(df)
