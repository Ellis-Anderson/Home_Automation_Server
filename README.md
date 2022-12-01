# Home Automation Server

## Background

This repo contains some code for setting up a home automation server controlling an rgb light.
I wanted the light to also act as a ["sunrise" alarm clock](https://www.wired.com/gallery/best-sunrise-alarm-clocks/).
Yep, I spent a lot of time and way more money to make a (probably) inferior product. Ya gotta love it.

Communication between web clients and the server is handled through [websockets](https://python-socketio.readthedocs.io/en/latest/).
Python-socketio has a flask wrapper, [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/), which was used directly.
Communication between the server and the alarm/other IOT devices is handled via [mqtt](https://github.com/eclipse/paho.mqtt.python).
Paho.mqtt.python similarly has a flask wrapper, [flask-mqtt](https://flask-mqtt.readthedocs.io/en/latest/).
The alarm function is handled via [apscheduler](https://apscheduler.readthedocs.io/en/3.x/) and its
flask wrapper [flask-apscheduler](https://viniciuschiele.github.io/flask-apscheduler/).

All of these packages also have flask wrappers which were used

## Setup

After cloning this repo you can install the necessary requirements for running the server with `pip install -r requirements.txt`.
Dev requirements can be installed with `pip install -r requirements-dev.txt`.
You can run the server yourself by calling `python wsgi.py`.
By default the server runs as `127.0.0.1:5002`.
