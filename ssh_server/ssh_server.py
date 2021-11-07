#!/usr/bin/env python

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import json
import time

from elasticsearch import Elasticsearch
from datetime import datetime
import geoip2.database

import paramiko
from paramiko.py3compat import b, u, decodebytes

es = Elasticsearch("elasticsearch:9200")

host = "0.0.0.0"
port = 22

# setup logging
paramiko.util.log_to_file("./log/ssh_server.log")

#wf = open('./log/auth.log', 'a')

# openssl genrsa > server.key
host_key = paramiko.RSAKey(filename="server.key")


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        clientip = self.clientip[0]
        dic = {}
        dic["date"] = now
        dic["username"] = username
        dic["password"] = password
        dic["clientip"] = clientip

        json_data = json.dumps(dic)

        print("[+] %s: from: %s, username: %s, password: %s" % (now, clientip, username, password))
        #wf.write("[+] %s: from: %s, username: %s, password: %s" % (now, clientip, username, password))
        #wf.flush()

        reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

        try:
            res = reader.city(clientip)
            dic["geo_point"] = {"lat":res.location.latitude, "lon": res.location.longitude}
            dic["country"] = res.country.iso_code
        except:
            pass

        json_data = json.dumps(dic)

        es.index(index="ssh", doc_type="_doc", body=json_data)
        time.sleep(1)

        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


def honeypot(client, addr):
    time.sleep(2)
    t = paramiko.Transport(client)

    t.local_version = 'SSH-2.0-OpenSSH_5.9'
    t.add_server_key(host_key)
    server = Server()
    server.clientip = addr
    try:
        t.start_server(server=server)
    except:
        pass

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
    except Exception as e:
        print("*** Bind failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        sock.listen(100)
        print("Listening for connection ...")
        while True:
            client, addr = sock.accept()

            handle_thread = threading.Thread(target=honeypot, args=(client, addr), daemon=True)
            handle_thread.start()

    except Exception as e:
        print("*** Listen/accept failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
