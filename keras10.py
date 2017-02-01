# keras10.py

# This script should use Keras, SQLAlchemy, and Flask-RESTful to generate stock market predictions.

# Demo:
# export FLASK_DEBUG=1
# ~/anaconda3/bin/python keras10.py
# curl localhost:5000/keras10/IBM/2016/9

import io
import keras
import pdb
import os
import flask         as fl
import flask_restful as fr
import pandas        as pd
import numpy         as np
import datetime      as dt
import sklearn.linear_model as skl
from sqlalchemy import create_engine

# I should connect to the DB
db_s = 'postgres://ann:ann@127.0.0.1/ann'
conn = create_engine(db_s).connect()

application = fl.Flask(__name__)
api         = fr.Api(application)

# This class should use get prices from Yahoo.
# Then it should generate predictions with sklearn.
class Keras10(fr.Resource):
  # I should tell get() about URL-path-tokens:
  def get(self, tkr='AAPL', yr2predict='2017', yrs2train=8):
    k1_s   = '1. You want to predict'
    k2_s   = '2. For this year'
    k3_s   = '3. By learning from this many years'
    k4_s   = '4. With '
    algo_s = 'Linear Regression'

    # I should get prices for tkr:
    prices0_df = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s='+tkr)

    # See diagram: py4.us/cclasses/class04#r2
    prices1_df = prices0_df[['Date','Close']].sort_values(['Date'])
    prices1_df.columns = ['Date','Price']
    
    # Create feat_df from prices1_df, pctlead, pctlag1    
    # See diagram: py4.us/cclasses/class04#r2
    feat_df = prices1_df.copy()
    feat_df['pctlead'] = (100.0 * (feat_df.Price.shift(-1) - feat_df.Price) / feat_df.Price).fillna(0)
    feat_df['pctlag1'] = feat_df.pctlead.shift(1).fillna(0)

    # I should copy test_yr-observations (about 252) from feat_df into test_yr_df.
    # See diagram: py4.us/cclasses/class04#r2
    test_start_sr = (feat_df.Date > yr2predict)
    test_end_sr   = (feat_df.Date < str(int(yr2predict)+1))
    test_yr_df    = feat_df.copy()[(test_start_sr & test_end_sr)]

    # I should copy train_i-years of observations before test_yr from feat_df into train_df
    # See diagram: py4.us/cclasses/class04#r2
    train_i        = yrs2train
    train_end_sr   = (feat_df.Date < yr2predict)
    train_start_i  = int(yr2predict) - train_i
    train_start_s  = str(train_start_i)
    train_start_sr = (feat_df.Date > train_start_s)
    train_df       = feat_df.copy()[ train_start_sr & train_end_sr ]
    
    # I should declare x_train to be train_df.pctlag1
    x_train = train_df.pctlag1
    # I should declare y_train to be train_df.pctlead
    y_train = train_df.pctlead
    # I should create a Linear Regression model
    linr_model = skl.LinearRegression()
    # I should use model to "fit" straight line to x_train and y_train
    x_train_a = np.array(x_train).reshape(-1, 1)
    y_train_a = np.array(y_train)
    linr_model.fit(x_train_a,y_train_a)

    # I should collect predictions for yr2predict
    xtest_a = np.array(test_yr_df.pctlag1).reshape(-1, 1)
    predictions_a = linr_model.predict(xtest_a)
    # See diagram: py4.us/cclasses/class04#r2
    predictions_l = predictions_a.tolist()
    # I should copy test_yr_df to predictions_df
    predictions_df = test_yr_df.copy()
    predictions_df['prediction'] = predictions_l
    predictions_df['eff'] = np.sign(predictions_df.prediction) * predictions_df.pctlead
    predictions_df['acc'] = (predictions_df.eff > 0).astype(int)

    # I should report Accuracy:
    len_i         = len(predictions_df)
    accuracy_f    = 100 *  predictions_df.acc.sum()/len_i
    lo_accuracy_f = 100 * (predictions_df.pctlead>0).astype(int).sum()/len_i
    # I should report Effectiveness:
    effectiveness_f    = predictions_df.eff.sum()
    lo_effectiveness_f = predictions_df.pctlead.sum()

    # I should talk to the End-User:
    return {k1_s:tkr
            ,k2_s:yr2predict
            ,k3_s:yrs2train
            ,k4_s:algo_s
            ,'5. Accuracy':                accuracy_f
            ,'6. Long Only Accuracy':      lo_accuracy_f
            ,'7. Effectiveness':           effectiveness_f
            ,'8. Long Only Effectiveness': lo_effectiveness_f
    }
# I should declare URL-path-tokens, and I should constrain them:
api.add_resource(Keras10, '/keras10/<tkr>/<yr2predict>/<int:yrs2train>')
# curl localhost:5010/keras10/SPY/2016/25


# This function should get dates and prices from Yahoo for a tkr.
# Then it should return a DF full of features.
def genf(tkr):
  # I should get closing-prices
  prices0_df         = pd.read_csv('http://ichart.finance.yahoo.com/table.csv?s='+tkr)
  feat_df = prices0_df[['Date','Close']].sort_values(['Date'])
  feat_df.columns = ['cdate','closep']
  pctlead_sr         = (100.0*(feat_df.closep.shift(-1) - feat_df.closep) / feat_df.closep).fillna(0)
  feat_df['pctlead'] = np.round(pctlead_sr,3)
  feat_df['updown']  = [int(pctlead > 0.0) for pctlead in feat_df.pctlead]
  
  # I should calculate pctlags:
  lags_l = [1,2,3,4,5,6,7,8,12,16]
  for lag_i in lags_l:
    pctlagx_sr = (100.0*(feat_df.closep - feat_df.closep.shift(lag_i))/feat_df.closep.shift(lag_i)).fillna(0)
    col_s      = 'pctlag'+str(lag_i)
    feat_df[col_s] = np.round(pctlagx_sr,4)
  # I should calculate mvg-avg slopes:
  slopes_l = [2,3,4,5,6,7,8,9]
  for slope_i in slopes_l:
    rollx          = feat_df.rolling(window=slope_i)
    col_s          = 'slope'+str(slope_i)
    slope_sr       = 100.0 * (rollx.mean().closep - rollx.mean().closep.shift(1))/rollx.mean().closep
    feat_df[col_s] = np.round(slope_sr,4)
  # I should generate Date features:
  dt_sr = pd.to_datetime(feat_df.cdate)
  dow_l = [float(dt.strftime('%w' ))/100.0 for dt in dt_sr]
  moy_l = [float(dt.strftime('%-m'))/100.0 for dt in dt_sr]
  feat_df['dow'] = dow_l
  feat_df['moy'] = moy_l
  return feat_df

# This class should use genf() to get prices and features for a tkr.
# Then it should generate predictions with Keras and save them to DB.
class Keras11(fr.Resource):
  # I should tell get() about URL-path-tokens:
  def get(self, local=False, tkr='SPY', yr2predict='2017', yrs2train=20, features = 'pctlag1,slope2,moy'):
    k1_s   = '1. You want to predict'
    k2_s   = '2. For this year'
    k3_s   = '3. By learning from this many years'
    k4_s   = '4. With '
    algo_s = 'Keras Logistic Regression'

    # I should get prices and features for tkr:
    if not local: # I should see fl.request.args
      features = fl.request.args.get('features', 'pctlag1,slope3,dom')
    features_l = features.split(',')
    col_l      = ['cdate','closep','pctlead','updown']+features_l
    feat_df    = genf(tkr)[col_l]

    # I should copy test_yr-observations (about 252) from feat_df into test_yr_df.
    test_start_sr = (feat_df.cdate > yr2predict)
    test_end_sr   = (feat_df.cdate < str(int(yr2predict)+1))
    test_yr_df    = feat_df.copy()[(test_start_sr & test_end_sr)]

    # I should copy train_i-years of observations before test_yr from feat_df into train_df
    train_i        = yrs2train
    train_end_sr   = (feat_df.cdate < yr2predict)
    train_start_i  = int(yr2predict) - train_i
    train_start_s  = str(train_start_i)
    train_start_sr = (feat_df.cdate > train_start_s)
    train_df       = feat_df.copy()[ train_start_sr & train_end_sr ]
    
    # I should declare x_train to be train_df.pctlag1
    x_train = train_df[features_l].fillna(0.0)
    # I should declare y_train to be train_df.pctlead
    y_train = train_df.pctlead
    # I should create a Linear Regression model
    # I should use model to "fit" straight line to x_train and y_train
    x_train_a = np.array(x_train)
    y_train_a = np.array(y_train)
    # I should use Keras to fit a model here.
    # Keras kmodel wants a 1-hot encoded class.
    ytrain1h_l = [[0,1] if updown else [1,0] for updown in train_df.updown]
    ytrain1h_a = np.array(ytrain1h_l).reshape(-1,2)
    kmodel     = keras.models.Sequential()
    features_i = len(features_l)
    kmodel.add(keras.layers.core.Dense(features_i, input_shape=(features_i,)))
    kmodel.add(keras.layers.core.Activation('relu'))
    kmodel.add(keras.layers.core.Dense(2)) # because I have 2 classes: up and down
    kmodel.add(keras.layers.core.Activation('softmax'))
    kmodel.compile(loss='categorical_crossentropy', optimizer='adam')
    kmodel.fit(x_train_a, ytrain1h_a, batch_size=1, nb_epoch=2)

    # I should collect predictions for yr2predict
    xtest_a       = np.array(test_yr_df[features_l].fillna(0.0))
    predictions_a = kmodel.predict(xtest_a)[:,1]
    predictions_l = predictions_a.tolist()
    # I should copy test_yr_df to predictions_df
    predictions_df = test_yr_df.copy()
    predictions_df['prediction'] = predictions_l
    predictions_df['eff'] = np.sign(predictions_df.prediction-0.5) * predictions_df.pctlead
    predictions_df['acc'] = (predictions_df.eff > 0).astype(int)

    # I should report Accuracy:
    len_i         = len(predictions_df)
    accuracy_f    = 100 *  predictions_df.acc.sum()/len_i
    lo_accuracy_f = 100 * (predictions_df.pctlead>0).astype(int).sum()/len_i
    # I should report Effectiveness:
    effectiveness_f    = predictions_df.eff.sum()
    lo_effectiveness_f = predictions_df.pctlead.sum()
    csv_s              = predictions_df.to_csv(index=False)

    # I should save predictions to DB:
    sql_s = '''create table if not exists predictions 
      (tkr        varchar
      ,yr2predict int
      ,yrs2train  int
      ,features   varchar
      ,effectiveness    float
      ,lo_effectiveness float
      ,accuracy         float
      ,lo_accuracy      float
      ,created_at       timestamp
      ,csv text)'''
    conn.execute(sql_s)

    sql_s = '''insert into predictions
      (tkr
      ,yr2predict
      ,yrs2train
      ,features
      ,effectiveness
      ,lo_effectiveness
      ,accuracy
      ,lo_accuracy
      ,created_at
      ,csv)
      values (%s,%s,%s,  %s,%s,%s,  %s,%s,now(), %s)'''
    conn.execute(sql_s
                 ,[tkr
                   ,int(yr2predict)
                   ,yrs2train
                   ,features
                   ,effectiveness_f
                   ,lo_effectiveness_f
                   ,accuracy_f
                   ,lo_accuracy_f
                   #, created_at supplied by postgres
                   ,csv_s])

    # I should talk to the End-User:
    return {k1_s:tkr
            ,k2_s:yr2predict
            ,k3_s:yrs2train
            ,k4_s:algo_s
            ,'5. Effectiveness':           effectiveness_f
            ,'6. Long Only Effectiveness': lo_effectiveness_f
            ,'7. Accuracy':                accuracy_f
            ,'8. Long Only Accuracy':      lo_accuracy_f
    }
# I should declare URL-path-tokens, and I should constrain them:
api.add_resource(Keras11, '/keras11/<tkr>/<yr2predict>/<int:yrs2train>')
# curl localhost:5010/keras11/SPY/2016/25

# This class should get predictions from DB.
class Keras12(fr.Resource):
  # I should tell get() about URL-path-tokens:
  def get(self, local=False, tkr='SPY', yr2predict='2017', yrs2train=20, features = 'pctlag1,slope2,moy'):

    k1_s   = '1. You want to predict'
    k2_s   = '2. For this year'
    k3_s   = '3. By learning from this many years'
    k4_s   = '4. With '
    algo_s = 'Keras Logistic Regression'

    # I should get prices and features for tkr:
    if not local: # I should see fl.request.args
      features = fl.request.args.get('features', 'pctlag1,slope3,dom')
    # I should get csv_s from db
    sql_s = '''select created_at,csv from predictions
      where tkr      = %s
      and yr2predict = %s
      and yrs2train  = %s
      and features   = %s
      order by created_at desc limit 1'''
    result = conn.execute(sql_s,[tkr,yr2predict,yrs2train,features])
    myrow      = [row for row in result][0]
    created_at = myrow['created_at']
    csv_s      = myrow['csv']
    predictions_df = pd.read_csv(io.StringIO(csv_s))

    # I should report Accuracy:
    len_i         = len(predictions_df)
    accuracy_f    = 100 *  predictions_df.acc.sum()/len_i
    lo_accuracy_f = 100 * (predictions_df.pctlead>0).astype(int).sum()/len_i
    # I should report Effectiveness:
    effectiveness_f    = predictions_df.eff.sum()
    lo_effectiveness_f = predictions_df.pctlead.sum()
    return {k1_s:tkr
            ,k2_s:yr2predict
            ,k3_s:yrs2train
            ,k4_s:algo_s
            ,'5. Effectiveness':           effectiveness_f
            ,'6. Long Only Effectiveness': lo_effectiveness_f
            ,'7. Accuracy':                accuracy_f
            ,'8. Long Only Accuracy':      lo_accuracy_f
            ,'9. created_at':              created_at
    }

api.add_resource(Keras12, '/keras12/<tkr>/<yr2predict>/<int:yrs2train>')
# curl localhost:5010/keras12/SPY/2016/25

# This class should try gettting predictions from DB.
# If not there, this class should get predictions from my Keras service.
# Demo:
# k13 = keras10.Keras13()
# oput = k13.get(local=True, tkr='SPY', yr2predict='2016', yrs2train=25, features='pctlag1,slope2,moy')

class Keras13(fr.Resource):
  # I should tell get() about URL-path-tokens:
  def get(self, local=False, tkr='SPY', yr2predict='2017', yrs2train=20, features = 'pctlag1,slope2,moy'):


    k1_s   = '1. You want to predict'
    k2_s   = '2. For this year'
    k3_s   = '3. By learning from this many years'
    k4_s   = '4. With '
    algo_s = 'Keras Logistic Regression'

    # I should get prices and features for tkr:
    if not local: # I should see fl.request.args
      features = fl.request.args.get('features', 'pctlag1,slope3,dom')
    # I should get csv_s from db
    sql_s = '''select created_at,csv from predictions
      where tkr      = %s
      and yr2predict = %s
      and yrs2train  = %s
      and features   = %s
      order by created_at desc limit 1'''
    result = conn.execute(sql_s,[tkr,yr2predict,yrs2train,features])
    # in sqlalchemy how to test if result is empty?
    # in sqlalchemy how to test for zero rows?
    # in sqlalchemy how to test for 0 rows?
    'bye'
    return {'under':'construction'}

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5010))
  application.run(host='0.0.0.0', port=port)
'bye'

