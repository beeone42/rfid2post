#!/usr/bin/python

import time, json, os, urllib2, serial

def read_config(confname):
    with open(confname) as json_data_file:
        data = json.load(json_data_file)
    return (data)

config = read_config("config.json")
port = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

def readrfid(port):
    data = ''
    while True:
        c = port.read()
        if c == '\n':
            return data
        data += c

while True:
    tag = readrfid(port)
    if tag == "\n" or tag == "":
        print "empty"
        pass;
    else:
        tag = tag.strip(' \t\n\r>-')
        if (tag != ""):
            print "tag: " + tag
