# ck.py

# This script shows how to import keras10.py.
# Then it accesses methods using Python rather than from Flask.

import keras10
import sys

k10 = keras10.SKService()
oput = k10.get(tkr='SPY', yr2predict='2016', yrs2train=25)
print(oput)
sys.exit()

k11 = keras10.KerasService()
oput = k11.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
print(oput)
k12 = keras10.DBService()
oput = k12.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
print(oput)

k13 = keras10.DBKerasService()
oput = k13.get(local=True, tkr='SPY', yr2predict='2011', yrs2train=24, features='pctlag1,slope2,dow,moy')
print(oput)
