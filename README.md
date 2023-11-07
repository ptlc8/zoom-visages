# Recherche de visages sur des photos

## Prérequis

### Linux

```sh
$ apt-get update 
$ apt-get install python3 python3-setuptools libgl1 libgl1-mesa-glx libglib2.0-0 python3-venv
```

## Installation

```sh
$ python3 -m venv venv
$ venv/bin/pip install flask opencv-python dlib
$ cd front
$ npm install
```

## Lancement en mode développement

```sh
$ cd front
$ npm run build
$ cd ..
$ venv/bin/python3 -m flask run
```

## Lancement en mode production avec Apache2

```sh
$ apt-get update
$ apt-get install apache2 libapache2-mod-wsgi-py3
$ a2enmod wsgi
$ cp apache2.conf /etc/apache2/sites-available/zoom-visages.conf
$ # edit zoom-visages.conf with your own path
$ a2ensite zoom-visages
$ service apache2 restart
```