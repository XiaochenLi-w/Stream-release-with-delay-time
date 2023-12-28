#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns

#plt.style.use("seaborn")
plt.style.use("seaborn-whitegrid")
# -------------------------------------------------------
color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(16, 3.5))

size = 5
x_label = ['Naive', 'Contin', 'Discontin', 'CompOrder', 'BucOrder']
x = np.arange(size)

total_width, n = 0.8, 2
width = total_width / n
x = x - (total_width - width) / 2

# Covid19
nosens_covid = [52809.72679324087 , 50998.35192082221 , 17028.91327399539 , 37250.33849176442 , 4236.0161494016775]
sens_covid = [35709.68973565579 , 29736.175743919914 , 9050.252104294517 , 23017.417151052367 , 4529.963681177834]

# Unemployment
nosens_une = [1216.8560268492888 , 1217.531596949159 , 383.9977729484272 , 762.9808050290695 , 214.45328196333875]
sens_une = [875.7351938114159 , 643.1370375821865 , 282.8302444244023 , 473.0357447803581 , 228.28277474682622]

# foodmart
nosens_food = [3123.2956466006985 , 3143.409976102276 , 1009.2703329547782 , 902.7512662383566 , 664.4819749313252]
sens_food = [1642.3413514614906 , 1047.6885937166871 , 706.9120998709743 , 806.1440017720811 , 718.004548367407]

# Outpatient
nosens_out = [4518389.266428379 , 4579760.043239072 , 1395960.208351309 , 1365578.2614101174 , 416605.0151946256]
sens_out = [1987950.0170170255 , 1650389.874434637 , 741596.2700887097 , 932854.8879109647 , 524240.3334394552]

ax1 = plt.subplot(1, 4, 1)
l1 = ax1.bar(x, nosens_covid,  width=width, label='No Sensitivity Reduce')
l2 = ax1.bar(x + width, sens_covid, width=width, label='Sensitivity Reduce')
#ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=15)
ax1.set_ylabel("MAE", fontsize=14)
ax1.set_title("COVID19 DEATH",y=-0.35, fontsize = 12)


ax2 = plt.subplot(1, 4, 2)
ax2.bar(x, nosens_une,  width=width, label='No Sensitivity Reduce')
ax2.bar(x + width, sens_une, width=width, label='Sensitivity Reduce')
#ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=15)
ax2.set_ylabel("MAE", fontsize=14)
ax2.set_title("Unemployment",y=-0.35, fontsize = 12)

ax3 = plt.subplot(1, 4, 3)
ax3.bar(x, nosens_food,  width=width, label='No Sensitivity Reduce')
ax3.bar(x + width, sens_food, width=width, label='Sensitivity Reduce')
#ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=15)
ax3.set_ylabel("MAE", fontsize=14)
ax3.set_title("Outpatient",y=-0.35, fontsize = 12)

ax4 = plt.subplot(1, 4, 4)
ax4.bar(x, nosens_food,  width=width, label='No Sensitivity Reduce')
ax4.bar(x + width, sens_food, width=width, label='Sensitivity Reduce')
#ax.bar(x + 2 * width, discontin_reduce, width=width, label='discontin_reduce')
plt.xticks(x + 0.25, x_label, rotation=15)
ax4.set_ylabel("MAE", fontsize=14)
ax4.set_title("Foodmart",y=-0.35, fontsize = 12)



legend_list = ['No Sensitivity Reduce', 'Sensitivity Reduce']
fig.legend([l1, l2], loc='center', labels = legend_list, bbox_to_anchor=(0.5, 0.95), ncol=2, prop={'size': 10}, frameon=True, edgecolor='gray')

fig.tight_layout()
fig.subplots_adjust(left = 0.054, bottom = 0.235, right = 0.979, top = 0.88, wspace = 0.264, hspace = 0.2)
plt.show()

filename = "Compare_sens_nosens"
fig.savefig(os.path.join("C:/Users/xiaoc/Dropbox/应用/Overleaf/streaming data releasing with delay/fig/experiment/comparison_all_datasets", filename + ".pdf"), dpi=3000)