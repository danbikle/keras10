# ck.py

# This script shows how to import keras10.py.
# Then it accesses methods using Python rather than from Flask.

import keras10

# k10 = keras10.Keras10()
# oput = k10.get(tkr='SPY', yr2predict='2016', yrs2train=25)
# print(oput)

# k11 = keras10.Keras11()
# oput = k11.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
# print(oput)
# k12 = keras10.Keras12()
# oput = k12.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
# print(oput)

k13 = keras10.Keras13()
oput = k13.get(local=True, tkr='SPY', yr2predict='2011', yrs2train=24, features='pctlag1,slope2,dow,moy')
print(oput)
