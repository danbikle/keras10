# README.md

This repo is a mix of technology to help end-users forecast the stock market closing price tomorrow:

  * Anaconda Python 4.2.0
  * Keras
  * SQLAlchemy
  * Flask-RESTful
  * Postgres 9.5

I intend for this repo to be deployed to a VirtualBox instance running Ubuntu 16.04.

I offer two types of instructions:

  * Simple Instructions
  * Detailed Instructions

I suggest that you follow the Simple Instructions.

# Simple Instructions

  * Install VirtualBox on your laptop
  * Import this VirtualBox Appliance:
  * https://drive.google.com/file/d/0Bx3iDDAtxxI4RVZuWmVZXzIxUWM
  * Above Appliance is 7.1 GB
  * Start the appliance and login as ann, passwd: a
  * Clone the keras10 repo with this shell syntax:
```bash
cd ~
git clone https://github.com/danbikle/keras10
```
  * Run the first demo with a simple shell command:
```bash
cd ~/keras10
python import_keras10.py
```
  * I did the above demo in my virtualbox and I saw this:
```bash
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ cd ~/keras10
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ python import_keras10.py
Using Theano backend.
Epoch 1/2
5774/5774 [==============================] - 1s - loss: 0.6958     
Epoch 2/2
5774/5774 [==============================] - 1s - loss: 0.6915     
I should get predictions from DB.
{'3. By learning from this many years': 24, '8. Long Only Accuracy': 50.19762845849802, '7. Accuracy': 50.19762845849802, '6. Long Only Effectiveness': -35.858000000000004, '4. With ': 'Keras Logistic Regression', '1. You want to predict': 'SPY', '5. Effectiveness': 28.391999999999992, '2. For this year': '2008'}
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ 
```

  * Run the next demo with a simple shell command:
```bash
cd ~/keras10
./flask10.bash
```

  * I did the above demo in my virtualbox and I saw this:
```bash
ann@ub16feb:~$ 
ann@ub16feb:~$ cd ~/keras10/
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ ./flask10.bash 
Using Theano backend.
 * Running on http://0.0.0.0:5010/ (Press CTRL+C to quit)
 * Restarting with stat
Using Theano backend.
 * Debugger is active!
 * Debugger pin code: 145-554-526
```

  * The above shell is running a webserver. You should leave it alone.
  * The next demo requires another shell. So, start another shell.
  * Run the next demo with a simple shell command:
```bash
cd ~/keras10
bash -x curlem.bash
```
  * I did the above demo in my virtualbox and I saw this:
```bash

ann@ub16feb:~$ 
ann@ub16feb:~$ cd ~/keras10
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$ bash -x curlem.bash
+ curl localhost:5010/skservice/SPY/2016/25
{
    "1. You want to predict": "SPY",
    "2. For this year": "2016",
    "3. By learning from this many years": 25,
    "4. With ": "Linear Regression",
    "5. Accuracy": 55.55555555555556,
    "6. Long Only Accuracy": 54.36507936507937,
    "7. Effectiveness": 28.21438991556794,
    "8. Long Only Effectiveness": 12.23161707633516
}
+ curl 'localhost:5010/keras/SPY/2016/25?features=pctlag1,pctlag2,slope2,slope4,dow,moy'
{
    "1. You want to predict": "SPY",
    "2. For this year": "2016",
    "3. By learning from this many years": 25,
    "4. With ": "Keras Logistic Regression",
    "5. Effectiveness": 17.058000000000014,
    "6. Long Only Effectiveness": 12.229999999999992,
    "7. Accuracy": 54.36507936507937,
    "8. Long Only Accuracy": 54.36507936507937
}
+ curl 'localhost:5010/db/SPY/2016/25?features=pctlag1,pctlag2,slope2,slope4,dow,moy'
{
    "1. You want to predict": "SPY",
    "2. For this year": "2016",
    "3. By learning from this many years": 25,
    "4. With ": "Keras Logistic Regression",
    "5. Effectiveness": 17.058000000000014,
    "6. Long Only Effectiveness": 12.229999999999995,
    "7. Accuracy": 54.36507936507937,
    "8. Long Only Accuracy": 54.36507936507937
}
+ curl 'localhost:5010/dbkeras/SPY/2016/25?features=pctlag1,pctlag2,slope2,slope4,dow,moy'
{
    "1. You want to predict": "SPY",
    "2. For this year": "2016",
    "3. By learning from this many years": 25,
    "4. With ": "Keras Logistic Regression",
    "5. Effectiveness": 17.058000000000014,
    "6. Long Only Effectiveness": 12.229999999999995,
    "7. Accuracy": 54.36507936507937,
    "8. Long Only Accuracy": 54.36507936507937
}
ann@ub16feb:~/keras10$ 
ann@ub16feb:~/keras10$
```

# Detailed Instructions

UNDER CONSTRUCTION
