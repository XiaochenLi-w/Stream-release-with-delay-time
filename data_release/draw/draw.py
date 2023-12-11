import argparse
import os

import matplotlib.pyplot as plt
import seaborn as sns
import yaml

plt.style.use("seaborn-whitegrid")

color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(7, 5))

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="D:/stream_delay/delay_code_github/Stream-release-with-delay-time/data_release/config/comparison_all.yml")

args = parser.parse_args()
with open(args.config, "r") as f:
    config = yaml.safe_load(f)

naive = config["naive"]
Order_based = config["Order_based"]
discontin_pp = config["discontin_pp"]
PeGaSus_delaypp = config["PeGaSus_delaypp"]
pegasus = config["pegasus"]
# contin_noisered = config["contin_noisered"]
order_adv = config["order_adv"]
contin_noisered_close = config["contin_noisered_close"]
discontin_reduce = config["discontin_reduce"]

x = config["epsilon_list"]

ax1 = plt.subplot(1,1,1)
# ax1.axis(ymin=0.75, ymax=0.85)
ax1.set_ylabel("MAE", fontsize = 14)
ax1.set_xlabel(r"$\epsilon$", fontsize = 14)
ax1.set_xticks(x)
# x = [1,2,3,4,5,6,7,8,9,10]
ax1.tick_params(axis="both", labelsize=13)
ax1.ticklabel_format(style='sci', scilimits=(0,5), axis='y')
ax1.set_title("Unemployment",y=-0.25, fontsize = 12)

l1 = ax1.plot(x,
              naive,
              label="naive",
              color=color_list[0],
              linestyle="-",
              marker="p",
              markersize=8,
              markerfacecolor='none')

l2 = ax1.plot(x,
             Order_based,
             label="Order_based",
             color=color_list[1],
             linestyle="-",
             marker="d",
             markersize=8,
             markerfacecolor='none')

l3 = ax1.plot(x,
             discontin_pp,
             label="discontin_pp",
             color=color_list[2],
             linestyle="-",
             marker="s",
             markersize=8,
             markerfacecolor='none')

l4 = ax1.plot(x,
             PeGaSus_delaypp,
             label="PeGaSus_delaypp",
             color=color_list[3],
             linestyle="-",
             marker="h",
             markersize=8,
             markerfacecolor='none')

l5 = ax1.plot(x,
             pegasus,
             label="pegasus",
             color=color_list[4],
             linestyle="-",
             marker="^",
             markersize=8,
             markerfacecolor='none')

# l6 = ax1.plot(x,
#              contin_noisered,
#              label="contin_noisered",
#              color=color_list[5],
#              linestyle="-",
#              marker="x",
#              markersize=8,
#              markerfacecolor='none')

l6 = ax1.plot(x,
             order_adv,
             label="contin_noisered",
             color=color_list[5],
             linestyle="-",
             marker="x",
             markersize=8,
             markerfacecolor='none')

l7 = ax1.plot(x,
             contin_noisered_close,
             label="contin_noisered_close",
             color=color_list[6],
             linestyle="-",
             marker=">",
             markersize=8,
             markerfacecolor='none')

l8 = ax1.plot(x,
             discontin_reduce,
             label="discontin_reduce",
             color=color_list[7],
             linestyle="-",
             marker="v",
             markersize=8,
             markerfacecolor='none')

legend_list = ["naive", "Order_based", "discontin_pp", "PeGaSus_delaypp", "pegasus", "order_advance", "contin_noisered", "discontin_reduce"]

fig.legend([l1, l2, l3, l4, l5, l6, l7, l8], labels =legend_list, loc='center', bbox_to_anchor=(0.5, 0.9), ncol=4, prop = {'size':10}, frameon = True, edgecolor = 'gray')

fig.tight_layout()
fig.subplots_adjust(left = 0.114, bottom = 0.182, right = 0.975, top = 0.794, wspace = 0.2, hspace = 0.2)
plt.show()

filename = "unemployment_all"
fig.savefig(os.path.join("C:/Users/xiaoc/Dropbox/应用/Overleaf/streaming data releasing with delay/fig/experiment/comparison_all_datasets/", filename + ".pdf"), dpi=3000)