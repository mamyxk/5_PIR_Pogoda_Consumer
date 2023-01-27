#!/usr/bin/bash

sudo apt install -y python3-pip

pip install pika
pip install requests

python3 main.py
