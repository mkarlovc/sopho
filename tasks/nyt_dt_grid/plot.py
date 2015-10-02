import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

df = pd.load(sys.argv[1])
plt.pcolor(df)
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
plt.show()

