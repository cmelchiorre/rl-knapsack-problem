import matplotlib.pyplot as plt

from ui.qtbstyles import *

plt.style.use(['dark_background'])
# print(plt.rcParams.keys())
# input()
plt.rcParams.update({
    "figure.facecolor":f"{COLOR_BACKGROUND_01}", 
    #"figure.edgecolor":f"white", 
    "axes.facecolor": f"{COLOR_BACKGROUND_02}", 
    "text.color": f"{COLOR_TEXT_LIGHTER}", 
    "axes.labelcolor": f"{COLOR_TEXT_LIGHTER}"
})


# create the figure and subplots
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,4))

import random

# Generate a list of 100 random floats between 0 and 1
values = [random.uniform(0, 1) for _ in range(100)]


# plot each list on its own subplot
axs[0].plot(values, color='green')
axs[0].set_title('Weights')
axs[0].set_ylabel('weight_history')

plt.show()