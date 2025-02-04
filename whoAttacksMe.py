#!/usr/bin/env python3

import geoip2.database
import os
import time
import socket
import signal
import readchar

LOG_FILE = "/var/log/kern.log"

def handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == 'y':
        print("")
        exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)

signal.signal(signal.SIGINT, handler)

def follow(name: str) -> str:
    current = open(name, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            yield line

        try:
            if os.stat(name).st_ino != curino:
                new = open(name, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                continue
        except IOError:
            pass
        time.sleep(1)

def getTimeAndIP(line: str) -> tuple:
    hostname = socket.gethostname()
    time = line.split(hostname)[0].strip()
    ip = line.split("SRC=")[1].split()[0]
    return time, ip

def main():
    with geoip2.database.Reader("/usr/share/GeoIP/GeoLite2-City.mmdb") as reader:
        for l in follow(LOG_FILE):
            if "iptables deny" in l:
                time, ip = getTimeAndIP(l)
                domain = '.'.join(ip.split('.')[:2])
                if domain in ['192.168']:
                    continue
                response = reader.city(ip)
                country = response.country.name
                region = response.subdivisions.most_specific.name
                city = response.city.name
                print(f"attack at {time} from IP {ip} -> {country}, {city}({region})")

if __name__ == "__main__":
    main()
