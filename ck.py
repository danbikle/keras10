# ck.py

# This script shows how to import keras10.py.
# Then it accesses methods using Python rather than from Flask.

import keras10

# k10 = keras10.Keras10()
# oput = k10.get(tkr='SPY', yr2predict='2016', yrs2train=25)
# print(oput)

k11 = keras10.Keras11()
oput = k11.get(tkr='SPY', yr2predict='2016', yrs2train=25)#, features='pctlag1,slope2')
print(oput)
