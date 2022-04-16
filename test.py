import pandas as pd
import numpy as np
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

import seaborn as sns

tmp = pd.DataFrame(0, index=[i for i in range(1, 10)], columns=[i for i in range(1, 4)])
tmp.iloc[5-1, 2-1] = 2  # cell [5][2]
tmp.iloc[4-1, 2-1] = 1  # cell [4][2]
tmp.iloc[3-1, 2-1] = 12  # cell [3][2]
tmp.iloc[2-1, 1-1] = 1  # cell [2][1]
tmp.iloc[3-1, 1-1] = 3  # cell [3][1]
tmp.iloc[3-1, 3-1] = 33  # cell [3][3]
tmp.iloc[7-1, 3-1] = 333  # cell [3][3]

print(tmp)

hist_row_non_zeros = (tmp != 0).sum(axis=1)
hist_row_non_zeros2 = hist_row_non_zeros
tt = tmp[hist_row_non_zeros > 3]
print('----\n', tt, '\n----')
print(hist_row_non_zeros)
print(tmp.shape[0])

exit()

tmp = pd.DataFrame(0, index=[i for i in range(1, 10)], columns=[i for i in range(1, 4)])
tmp.iloc[5-1, 2-1] = 2  # cell [5][2]
tmp.iloc[4-1, 2-1] = 1  # cell [4][2]
tmp.iloc[3-1, 2-1] = 12  # cell [3][2]
tmp.iloc[2-1, 1-1] = 1  # cell [2][1]
tmp.iloc[3-1, 1-1] = 3  # cell [3][1]

print(tmp)

# print(np.linalg.norm(tmp, axis=0))
print((tmp != 0).sum())
tmp = tmp.loc[:, ((tmp != 0).sum() > 2500)]  # filter cols with less than different 2500 different gens
print(tmp)

sns.distplot(tmp.sum(axis=1), hist=True)
plt.show()

tmp.to_csv('tmp777.csv')


# tmp = np.zeros((10, 3), dtype=np.int)
# tmp[5, 2] = 999  # cell [5][2]
# # np.savetxt("tmp1115.csv", tmp, delimiter = ",", fmt="%.0f", header="A, B",  comments="")
# df = pd.DataFrame(tmp)
# df.drop([0], inplace=True, axis=0)
# df.drop([0], inplace=True, axis=1)
# df.to_csv('tmp999.csv')
print("Done")

