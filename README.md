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

