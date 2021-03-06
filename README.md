# Final Year Project: The prediction of currency exchange rates using Deep Learning (LSTM)

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
    
    - JavaScript / jQuery
    
    - Chart.js
    
    
  - <b>Currency Conversion & Currency Exchange Rates</b>
  
    - JSON Dataset (Open-Source API)
    
      - FXMarketAPI
      
      - Exchange Rates API
    

  - <b>Storage</b>

    - MongoDB
  
      - Flask-PyMongo (Python package)


  - <b>Job Scheduler</b>

    - APScheduler (Python package) 
    
  
  - <b>Real Time</b>
  
    - SocketIO
  
      - Flask-SocketIO (Python package)


  - <b>Machine Learning & Deep Learning</b>
  
    - Tensorflow 2 / Keras
    
    - Scikit-learn

    - HDF5 

<br>

#### System Architecture 
  
  ![System_v6](https://user-images.githubusercontent.com/33058365/110205822-1fcf8f80-7e72-11eb-9c67-3d2acf5700ec.png)


<br>
<br>
  
### Environment:

#### Configure Setting

##### In the directory (/Development)

```
pip3 install virtualenv
virtualenv env -p python3
```

#### Configure Virtual Environment

##### Activate

###### For Ubuntu

```
. env/bin/activate
```

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

  - <b>Cloud Server</b>

    - AWS

      - Instance OS (Ubuntu:18.04)

    
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

#### Configure Setting

##### In the AWS EC2 Instance directory (/home/ubuntu)

#### Git clone repository

```
git clone https://github.com/D17123466/Project.git
```

#### Install all required packages
###### Ubuntu, Python, Flask, Tensorflow, MongoDB, Gunicorn, Nginx...

```
cd Project/Deployment
sh init.sh
```

#### Configure Gunicorn & Nginx

```
sh start_ip.sh <AWS Instance Public IP>
```

#### Open

> (AWS Instance Public IP)

#### Stop

```
sh end.sh
```

