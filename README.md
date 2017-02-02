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
  * Install flask-restful from conda-forge into Anaconda:
```bash
conda install -c conda-forge flask-restful
```
