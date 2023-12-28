import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
import yaml

plt.style.use("seaborn-whitegrid")

color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(16, 3.5))

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="D:/stream_delay/delay_code_v2/draw/config/compare_all_nosens.yml")

args = parser.parse_args()
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

naive_foot = config["naive_foot"]
Order_based_foot = config["Order_based_foot"]
discontin_pp_foot = config["discontin_pp_foot"]
PeGaSus_delaypp_foot = config["PeGaSus_delaypp_foot"]
pegasus_foot = config["pegasus_foot"]
order_adv_foot = config["order_adv_foot"]
contin_noisered_close_foot = config["contin_noisered_close_foot"]
discontin_reduce_foot = config["discontin_reduce_foot"]

naive_une = config["naive_une"]
Order_based_une = config["Order_based_une"]
discontin_pp_une = config["discontin_pp_une"]
PeGaSus_delaypp_une = config["PeGaSus_delaypp_une"]
pegasus_une = config["pegasus_une"]
order_adv_une = config["order_adv_une"]
contin_noisered_close_une = config["contin_noisered_close_une"]
discontin_reduce_une = config["discontin_reduce_une"]

naive_cus = config["naive_cus"]
Order_based_cus = config["Order_based_cus"]
discontin_pp_cus = config["discontin_pp_cus"]
PeGaSus_delaypp_cus = config["PeGaSus_delaypp_cus"]
pegasus_cus = config["pegasus_cus"]
order_adv_cus = config["order_adv_cus"]
contin_noisered_close_cus = config["contin_noisered_close_cus"]
discontin_reduce_cus = config["discontin_reduce_cus"]

naive_covid = config["naive_covid"]
Order_based_covid = config["Order_based_covid"]
discontin_pp_covid = config["discontin_pp_covid"]
PeGaSus_delaypp_covid = config["PeGaSus_delaypp_covid"]
pegasus_covid = config["pegasus_covid"]
order_adv_covid = config["order_adv_covid"]
contin_noisered_close_covid = config["contin_noisered_close_covid"]
discontin_reduce_covid = config["discontin_reduce_covid"]

x = config["epsilon_list"]

#------------------------------------------------------
ax1 = plt.subplot(1,4,1)
# ax1.axis(ymin=0.75, ymax=0.85)
ax1.set_ylabel("MAE", fontsize = 14)
ax1.set_xlabel(r"$\epsilon$", fontsize = 14)
ax1.set_xticks(x)
# x = [1,2,3,4,5,6,7,8,9,10]
ax1.tick_params(axis="both", labelsize=13)
ax1.ticklabel_format(style='sci', scilimits=(0,5), axis='y')
ax1.set_title("COVID19 DEATH",y=-0.35, fontsize = 12)

l1 = ax1.plot(x,
              naive_covid,
              label="naive_covid",
              color=color_list[0],
              linestyle="-",
              marker="p",
              markersize=8,
              markerfacecolor='none')

l2 = ax1.plot(x,
             Order_based_covid,
             label="Order_based_covid",
             color=color_list[1],
             linestyle="-",
             marker="d",
             markersize=8,
             markerfacecolor='none')

l3 = ax1.plot(x,
             discontin_pp_covid,
             label="discontin_pp_covid",
             color=color_list[2],
             linestyle="-",
             marker="s",
             markersize=8,
             markerfacecolor='none')

l4 = ax1.plot(x,
             PeGaSus_delaypp_covid,
             label="PeGaSus_delaypp_covid",
             color=color_list[3],
             linestyle="-",
             marker="h",
             markersize=8,
             markerfacecolor='none')

l5 = ax1.plot(x,
             pegasus_covid,
             label="pegasus_covid",
             color=color_list[4],
             linestyle="-",
             marker="^",
             markersize=8,
             markerfacecolor='none')

l6 = ax1.plot(x,
             order_adv_covid,
             label="contin_noisered",
             color=color_list[5],
             linestyle="-",
             marker="x",
             markersize=8,
             markerfacecolor='none')

l7 = ax1.plot(x,
             contin_noisered_close_covid,
             label="contin_noisered_close",
             color=color_list[6],
             linestyle="-",
             marker=">",
             markersize=8,
             markerfacecolor='none')

l8 = ax1.plot(x,
             discontin_reduce_covid,
             label="discontin_reduce",
             color=color_list[7],
             linestyle="-",
             marker="v",
             markersize=8,
             markerfacecolor='none')

#------------------------------------------------------
ax2 = plt.subplot(1,4,2)
# ax2.axis(ymin=0.75, ymax=0.85)
ax2.set_ylabel("MAE", fontsize = 14)
ax2.set_xlabel(r"$\epsilon$", fontsize = 14)
ax2.set_xticks(x)
# x = [1,2,3,4,5,6,7,8,9,10]
ax2.tick_params(axis="both", labelsize=13)
ax2.ticklabel_format(style='sci', scilimits=(0,5), axis='y')
ax2.set_title("Unemployment",y=-0.35, fontsize = 12)

l1 = ax2.plot(x,
              naive_une,
              label="naive_une",
              color=color_list[0],
              linestyle="-",
              marker="p",
              markersize=8,
              markerfacecolor='none')

l2 = ax2.plot(x,
             Order_based_une,
             label="Order_based_une",
             color=color_list[1],
             linestyle="-",
             marker="d",
             markersize=8,
             markerfacecolor='none')

l3 = ax2.plot(x,
             discontin_pp_une,
             label="discontin_pp_une",
             color=color_list[2],
             linestyle="-",
             marker="s",
             markersize=8,
             markerfacecolor='none')

l4 = ax2.plot(x,
             PeGaSus_delaypp_une,
             label="PeGaSus_delaypp_une",
             color=color_list[3],
             linestyle="-",
             marker="h",
             markersize=8,
             markerfacecolor='none')

l5 = ax2.plot(x,
             pegasus_une,
             label="pegasus_une",
             color=color_list[4],
             linestyle="-",
             marker="^",
             markersize=8,
             markerfacecolor='none')

l6 = ax2.plot(x,
             order_adv_une,
             label="contin_noisered",
             color=color_list[5],
             linestyle="-",
             marker="x",
             markersize=8,
             markerfacecolor='none')

l7 = ax2.plot(x,
             contin_noisered_close_une,
             label="contin_noisered_close",
             color=color_list[6],
             linestyle="-",
             marker=">",
             markersize=8,
             markerfacecolor='none')

l8 = ax2.plot(x,
             discontin_reduce_une,
             label="discontin_reduce",
             color=color_list[7],
             linestyle="-",
             marker="v",
             markersize=8,
             markerfacecolor='none')

#------------------------------------------------------
ax3 = plt.subplot(1,4,3)
# ax3.axis(ymin=0.75, ymax=0.85)
ax3.set_ylabel("MAE", fontsize = 14)
ax3.set_xlabel(r"$\epsilon$", fontsize = 14)
ax3.set_xticks(x)
# x = [1,2,3,4,5,6,7,8,9,10]
ax3.tick_params(axis="both", labelsize=13)
ax3.ticklabel_format(style='sci', scilimits=(0,5), axis='y')
ax3.set_title("Outpatient",y=-0.35, fontsize = 12)

l1 = ax3.plot(x,
              naive_cus,
              label="naive_cus",
              color=color_list[0],
              linestyle="-",
              marker="p",
              markersize=8,
              markerfacecolor='none')

l2 = ax3.plot(x,
             Order_based_cus,
             label="Order_based_cus",
             color=color_list[1],
             linestyle="-",
             marker="d",
             markersize=8,
             markerfacecolor='none')

l3 = ax3.plot(x,
             discontin_pp_cus,
             label="discontin_pp_cus",
             color=color_list[2],
             linestyle="-",
             marker="s",
             markersize=8,
             markerfacecolor='none')

l4 = ax3.plot(x,
             PeGaSus_delaypp_cus,
             label="PeGaSus_delaypp_cus",
             color=color_list[3],
             linestyle="-",
             marker="h",
             markersize=8,
             markerfacecolor='none')

l5 = ax3.plot(x,
             pegasus_cus,
             label="pegasus_cus",
             color=color_list[4],
             linestyle="-",
             marker="^",
             markersize=8,
             markerfacecolor='none')

l6 = ax3.plot(x,
             order_adv_cus,
             label="contin_noisered",
             color=color_list[5],
             linestyle="-",
             marker="x",
             markersize=8,
             markerfacecolor='none')

l7 = ax3.plot(x,
             contin_noisered_close_cus,
             label="contin_noisered_close",
             color=color_list[6],
             linestyle="-",
             marker=">",
             markersize=8,
             markerfacecolor='none')

l8 = ax3.plot(x,
             discontin_reduce_cus,
             label="discontin_reduce",
             color=color_list[7],
             linestyle="-",
             marker="v",
             markersize=8,
             markerfacecolor='none')

#-----------------------------------------
ax4 = plt.subplot(1,4,4)
# ax2.axis(ymin=0.75, ymax=0.85)
ax4.set_ylabel("MAE", fontsize = 14)
ax4.set_xlabel(r"$\epsilon$", fontsize = 14)
ax4.set_xticks(x)
# x = [1,2,3,4,5,6,7,8,9,10]
ax4.tick_params(axis="both", labelsize=13)
ax4.ticklabel_format(style='sci', scilimits=(0,5), axis='y')
ax4.set_title("Foodmart",y=-0.35, fontsize = 12)

l1 = ax4.plot(x,
              naive_foot,
              label="naive_foot",
              color=color_list[0],
              linestyle="-",
              marker="p",
              markersize=8,
              markerfacecolor='none')

l2 = ax4.plot(x,
             Order_based_foot,
             label="Order_based_foot",
             color=color_list[1],
             linestyle="-",
             marker="d",
             markersize=8,
             markerfacecolor='none')

l3 = ax4.plot(x,
             discontin_pp_foot,
             label="discontin_pp_foot",
             color=color_list[2],
             linestyle="-",
             marker="s",
             markersize=8,
             markerfacecolor='none')

l4 = ax4.plot(x,
             PeGaSus_delaypp_foot,
             label="PeGaSus_delaypp_foot",
             color=color_list[3],
             linestyle="-",
             marker="h",
             markersize=8,
             markerfacecolor='none')

l5 = ax4.plot(x,
             pegasus_foot,
             label="pegasus_foot",
             color=color_list[4],
             linestyle="-",
             marker="^",
             markersize=8,
             markerfacecolor='none')

l6 = ax4.plot(x,
             order_adv_foot,
             label="contin_noisered",
             color=color_list[5],
             linestyle="-",
             marker="x",
             markersize=8,
             markerfacecolor='none')

l7 = ax4.plot(x,
             contin_noisered_close_foot,
             label="contin_noisered_close",
             color=color_list[6],
             linestyle="-",
             marker=">",
             markersize=8,
             markerfacecolor='none')

l8 = ax4.plot(x,
             discontin_reduce_foot,
             label="discontin_reduce",
             color=color_list[7],
             linestyle="-",
             marker="v",
             markersize=8,
             markerfacecolor='none')



legend_list = ["Naive", "CompOrder", "Discontin_pp", "PeGaSus_Delay", "Pegasus", "BucOrder", "Contin_reduce", "Discontin_reduce"]

fig.legend([l1, l2, l3, l4, l5, l6, l7, l8], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.9), ncol=8, prop = {'size':10}, frameon = True, edgecolor = 'gray')

fig.tight_layout()
fig.subplots_adjust(left = 0.054, bottom = 0.235, right = 0.979, top = 0.805, wspace = 0.264, hspace = 0.2)
plt.show()

filename = "comp_all"
fig.savefig(os.path.join("C:/Users/xiaoc/Dropbox/应用/Overleaf/streaming data releasing with delay/fig/experiment/comparison_all_datasets/", filename + ".pdf"), dpi=3000)