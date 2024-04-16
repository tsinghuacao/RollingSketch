"""
-*- coding: utf-8 -*-
@File  : M_RS+BP.py
@author: XXX
@Time  : 2024/03/06 16:24
"""

import mmh3
import xxhash
import pandas as pd
import numpy as np
import random
from Component import *
from Set_parameter import *
import time


class LinearCounting:
    def __init__(self, m, win):
        self.m = m
        self.win = win
        self.LC = []

    def generate_lc(self):
        for i in range(self.m):
            self.LC.append(Node(0))

    def get_index(self, dst):
        res = xxhash.xxh64_intdigest(dst, seed=20240417)
        return res

    def get_es(self):
        res = -self.m*np.log((self.m-lru.head.val)/self.m)
        return res

    def get_ave_gap(self):
        sum = 0
        for i in range(self.m):
            sum+=self.LC[i].gap
        return sum/self.m

    def update(self, lru, CM, source, real_num):
        global row_length, print_LC_gap
        LC_estimate = []; cnt = 0; cnt_out = 0; es_out = []; ave_gap = []; cost_time = []
        for i in range(row_length):
            # time1_start = time.time()
            hash_val = self.get_index(source[i])
            bit_index = hash_val % self.m
            bit_val = self.LC[bit_index].val
            CM.CM_update(bit_index)
            if bit_val == 0:
                self.LC[bit_index].val = 1
                lru.head.val += 1
                lru.add_last(self.LC[bit_index])
            else:
                self.LC[bit_index].pre.gap += (self.LC[bit_index].gap + 1)
                self.LC[bit_index].gap = 0
                lru.shift_node(self.LC[bit_index])
            # time1_end = time.time()
            if cnt >= self.win:
                first_node_index = self.LC.index(lru.head.next)
                e_mode = lru.head.gap
                # time2_start = time.time()
                if e_mode == 0:
                    temp_flag1 = min(CM.CM_decrease(str(first_node_index)))
                    if temp_flag1 <= 0:
                        lru.head.gap = self.LC[first_node_index].gap
                        self.LC[first_node_index].gap = 0
                        self.LC[first_node_index].val = 0
                        lru.remove_old_node()
                        lru.head.val -= 1
                else:
                    while True:
                        hpos = random.randint(0, self.m-1)
                        hf = min(CM.get_CM_value(hpos))
                        if hf > 1:
                            break
                    CM.CM_decrease(hpos)
                    lru.head.gap -= 1

def Prepare(file_csv, file_real):
    df_source = pd.read_csv(file_csv, usecols=['src'])
    source = df_source['src']
    df_real = pd.read_csv(file_real, usecols=['real-cardinality'])
    real_num = df_real['real-cardinality']
    return source, real_num

def save_estimate(res, file_realnum):
    data = {'LC_estimate': res}
    df = pd.DataFrame(data)
    save_path = file_realnum[:-12]
    df.to_csv(save_path + '_LC_estimate.csv')


if __name__ == '__main__':
    global CM_para_d, CM_para_w, LC_para_m, where_datastream, where_stream_realcar, window_size
    lru = DoubleLinkedList()
    CM = CountMin(d=CM_para_d, w=CM_para_w)
    CM.generate_countmin()
    file_path = where_datastream
    file_realnum = where_stream_realcar
    source, real_num = Prepare(file_csv=file_path, file_real=file_realnum)
    LC = LinearCounting(m=LC_para_m, win=window_size)
    LC.generate_lc()
    es = LC.update(lru=lru, CM=CM, source=source, real_num=real_num)
    # save_estimate(es, file_realnum)







