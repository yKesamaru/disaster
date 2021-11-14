# How to use Docker
## Make sure you have git and Docker installed.
```bash:
$ which git
/usr/bin/git

$ which docker
/usr/bin/docker
```

## Download Disaster
```bash
$ git clone https://github.com/yKesamaru/disaster.git
$ cd disaster
```
## Make image from dockerfile
```bash
$ docker build -t disaster .
```
## Check the completed image
```bash
$ docker images
REPOSITORY                            TAG              IMAGE ID       CREATED         SIZE
disaster                              latest           8bb1b3c399ac   9 seconds ago   3.05GB
```
## Start Disaster
```bash
$ docker run disaster
 * Serving Flask app 'main.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:5000/ (Press CTRL+C to quit)
```
Access <strong> http://172.17.0.2:5000/ </strong> with your browser. 

# About the appearance
## Responsive design mode  
If you access http://172.17.0.2:5000/ with a browser, the display will be as follows.   
![top_page](img/top_page.png)  
Turn on browser's responsive design mode.  
![responsive](img/responsive.png)  

# Upload photos
Photos for the experiment are attached in advance.
These photos are `disaster/photos`.


