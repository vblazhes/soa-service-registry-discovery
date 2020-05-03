import configparser

import netifaces
import requests
from consul import Consul, Check
from fastapi import FastAPI

consul_port = 8500
service_name = "service2"
service_port = 8020


def get_ip():
    config_parser = configparser.ConfigParser()
    config_file = "config.ini"
    config_parser.read(config_file)
    interface_name = config_parser['NETWORK']['interface']
    ip = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]["addr"]
    return ip


def register_to_consul():
    consul = Consul(host="consul", port=consul_port)

    agent = consul.agent

    service = agent.service

    ip = get_ip()

    check = Check.http(f"http://{ip}:{service_port}/", interval="10s", timeout="5s", deregister="1s")

    service.register(service_name, service_id=service_name, address=ip, port=service_port, check=check)


def get_service(service_id):
    consul = Consul(host="consul", port=consul_port)

    agent = consul.agent

    service_list = agent.services()

    service_info = service_list[service_id]

    return service_info['Address'], service_info['Port']


app = FastAPI()

# register_to_consul()

print("OK service2")


@app.get("/")
def index():
    return "Service2"


@app.get("/text")
def get_text(lines: int = 3):
    address, port = get_service("service1")

    text = ""

    for i in range(lines):
        sentence = requests.get(f"http://{address}:{port}/sentence-independent").json()

        sentence = sentence["sentence"]

        text += sentence + "\n"

    text = text.strip()

    return {"text": text}


@app.get("/words")
def get_words():
    return {"words": ["fastapi", "consul", "python", "exception", "rest", "service", "discovery"]}
