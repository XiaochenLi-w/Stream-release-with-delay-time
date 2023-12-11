#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn")
# -------------------------------------------------------
color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(7, 5))

ax = plt.subplot(1, 1, 1)
size = 5
x_label = ['w=20', 'w=40', 'w=60', 'w=80', 'w=100']
x = np.arange(size)

#It is the results of D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/COVID19 DEATH.csv
# Order_based: [14112.56282767828, 24494.5534141015, 30485.514851654305, 34770.82123141321, 34061.30612199389]
# discontin_pp = [30772.100881663362, 24009.2143747081, 21826.135904685776, 18823.228306266283, 17786.83515658088]
# discontin_reduce = [14741.713947567612, 9942.481275942286, 8396.972936322181, 7108.99477980535, 7683.512097951765]
# order_adv = [5230.0663842870945, 5031.520666490756, 5624.445866987107, 5701.524378893998, 6221.503609246191]

#It is the results of D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/data/unemployment.csv
# Order_based: [447.07435786988833, 476.7888764328004, 585.904221383598, 510.2626371587079, 601.3932554078098]
discontin_pp = [603.4488906536606, 466.51952314686787, 415.96223266209915, 367.18254367281094, 336.95972050436575]
discontin_reduce = [289.1470256033074, 187.5751366347069, 153.19911438109528, 124.44588281237516, 112.78097052135399]
order_adv = [89.62928542482082, 97.02449358074753, 111.1493665540457, 119.13964230469358, 131.32969905401313]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

ax.bar(x, order_adv,  width=width, label='Order_advance')
ax.bar(x + width, discontin_pp, width=width, label='discontin_pp')
ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=0)
ax.set_ylabel("MAE", fontsize=14)
ax.set_xlabel("Length of Delay Time", fontsize=12)
fig.legend(loc='center', bbox_to_anchor=(0.5, 0.8), ncol=1, prop={'size': 10}, frameon=True, edgecolor='gray')
plt.show()

filename = "Compare_disgroup_orderadv_unemployment"
fig.savefig(os.path.join("C:/Users/xiaoc/Dropbox/应用/Overleaf/streaming data releasing with delay/fig/experiment/compare_group_order/", filename + ".pdf"), dpi=3000)