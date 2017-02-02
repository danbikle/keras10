# import_keras10.py

# This script shows how to import keras10.py.
# Then it accesses methods using Python rather than from Flask.

# Demo:
# python import_keras10.py

import keras10

s10 = keras10.SKService()
oput = s10.get(tkr='SPY', yr2predict='2016', yrs2train=25)
#print(oput)

s11 = keras10.KerasService()
oput = s11.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
#print(oput)

s12 = keras10.DBService()
oput = s12.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')
# print(oput)

s13 = keras10.DBKerasService()
oput = s13.get(local=True, tkr='SPY', yr2predict='2008', yrs2train=24, features='pctlag1,slope2,dow,moy')
print(oput)
