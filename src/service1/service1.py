import configparser

import netifaces
import requests
from consul import Consul, Check
from fastapi import FastAPI
from lorem.text import TextLorem

consul_port = 8500
service_name = "service1"
service_port = 8010


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

print("OK service1")


@app.get("/")
def index():
    return "Service1"


@app.get("/sentence-dependent")
def get_sentence_using_service_2():
    address, port = get_service("service2")

    words = requests.get(f"http://{address}:{port}/words").json()

    words = words["words"]

    lorem = TextLorem(words=words)

    return {"sentence": lorem.sentence()}


@app.get("/sentence-independent")
def get_sentence_using_own_words():
    lorem = TextLorem()

    return {"sentence": lorem.sentence()}
