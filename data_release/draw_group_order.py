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
x_label = ['w=10', 'w=30', 'w=50', 'w=70', 'w=90']
x = np.arange(size)

# --covid 19--
# Order_based = [11978.494952239902, 20350.66892043796, 29643.457023743424, 31013.610923782493, 39759.74804976777]
# discontin_pp = [37672.33456404817, 26000.973990076305, 21321.99714441007, 18683.994563670298, 18339.47202286061]
# discontin_reduce = [21573.444836422732, 12394.935923403184, 9412.705321965177, 8072.507045355063, 8177.207755787356]

# --unemployment---
Order_based = [412.8445900794568, 462.1118407738718, 384.95453045577233, 441.60462811471996, 697.3735209503906]
discontin_pp = [779.851030005173, 534.5653349789953, 440.91603491422967, 388.10713825146655, 341.97414663895466]
discontin_reduce = [449.3609951550522, 221.7993941069396, 165.46648926266442, 134.11885319901484, 120.76521184511648]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

ax.bar(x, Order_based,  width=width, label='Order_based')
ax.bar(x + width, discontin_pp, width=width, label='discontin_pp')
ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=0)
ax.set_ylabel("MAE", fontsize=14)
ax.set_xlabel("Length of Delay Time", fontsize=12)
fig.legend(loc='center', bbox_to_anchor=(0.5, 0.8), ncol=1, prop={'size': 10}, frameon=True, edgecolor='gray')
plt.show()

filename = "Compare_disgroup_order_unemployment"
fig.savefig(os.path.join("C:/Users/xiaoc/Dropbox/应用/Overleaf/streaming data releasing with delay/fig/experiment/compare_group_order/", filename + ".pdf"), dpi=3000)