# Final Year Project

## Demo:

### This is the directory in terms of demo for Interim Demo Version. It is the work that is used to provide the simple purpose of this Final Year Project. 

#### This demo is explained displaying the followings:

  - The line graph that shows the prediction of currency exchange rate (based EURO as default).

<br>
<br>


## Development:

### This is the directories where the project bas been being developed.

#### This development has technologies the followings:

  - <b>Web Development</b>
  
    - Flask (Python web framework)
    
    - HTML 
    
    - CSS / Bootstrap
    
    - JavaScript (Chart.js)
    
    
  - <b>Currency Conversion & Currency Exchange Rates</b>
  
    - Json Dataset (Free version API from an external source)
    

  - <b>Storage</b>

    - MongoDB


  - <b>Job Scheduler</b>

    - APScheduler (Python package) 


  - <b>Deep Learning</b>
  
    - Tensorflow 2 / Keras

    - HDF5 
  

<br>
<br>
  
### Environment:

#### Init Setting

##### In the directory (/Development)

```
pip3 install virtualenv
virtualenv env -p python3
```

#### Virtual Environment

##### Activate

###### For Ubuntu

'''
. env/bin/activate
'''

###### For Mac OS

```
source env/bin/activate
```

###### For Windows

```
env\bin\activate
```

##### Deactivate

```
deactivate
```

#### Install The Required Packages

```
pip install -r requirements.txt
```

#### Run 

```
python app.py
```

#### Open

> [http://0.0.0.0:5000/](http://0.0.0.0:5000/)

<br>
<br>

## Deployment:

### This is the directories where the project bas been deployed on a cloud server.

#### This deployment has the technologies the followings:

  - <b>Instance Operating System</b>

    - Ubuntu:18.04

    
  - <b>Web Application Server</b>
  
    - Gunicorn
    

  - <b>Web Server</b>

    - Nginx
  
  
  - <b>Container</b>

    - Docker (In Progress)

      - At the moment, bash files are used instead of docker container in order to get softwares to run reliably.

<br>
<br>

### Environment:

#### Init Setting

##### In the directory (/home/ubuntu)

##### Git clone repository

```
git clone https://github.com/D17123466/Project.git
```

##### Install all required packages
###### Ubuntu, Python, Flask, Tensorflow, MongoDB, Gunicorn, Nginx...

'''
cd Project/Deployment
sh init.sh
'''

#### Configure Gunicorn

'''
sh flask-conf.sh
'''

#### Configure Nginx

'''
sh nginx-conf.sh <AWS Instance Public IP>
'''

#### Open (Stopping)

> [AWS Instance Public IP]
