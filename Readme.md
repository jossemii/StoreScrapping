## Table of Contents
1. [Requirements](#requirements)
2. [How to install it](#how-to-install-it)
3. [How to use it](#how-to-use-it)
### Requirements
***
For run this proyect only Docker is needed.
## How to install it
***
A little intro about the installation. 
```
$ git clone https://github.com/josemibnf/SHALION-scrapping.git
$ cd ../SHALION-scrapping
$ docker build -t scraper .
```
## How to use it
***
Using the REST server 
(using python3 interpreter with requests lib,
 you can use postman).
```
$ docker run -d -p 8080:8080 scraper
$ python3
$ import requests
$ requests.get('http://localhost:8080/', json={'keywords': ['red', 'blue', 'green']}).json()
```
If docker raise a port error on the first step, other port can be used by:
```
$ docker run -d -p other_port:8080 scraper
$ requests.get('http://localhost:other_port/', ....
```


Working inside it with files
```
$ docker run -it --entrypoint /bin/bash scraper
$ cd src/
$ nano input.json
$ python3 usefiles.py
$ cat output.json
```
