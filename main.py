#!/usr/bin/python -W

import time, json, os, urllib2, serial, requests, logging

# prevent SSL/HTTPS warnings
logging.captureWarnings(True)

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
            url = config['rfid_login_api'] + tag
            f = urllib2.urlopen(url)
            readjson = json.loads(f.read())
            print readjson
            # {u'status': 0, u'message': u'Everything ok', u'data': {u'uid': u'sbenoit', u'uuid': u'13072'}} 
            # {u'status': 1, u'message': u'Unable to find the user.', u'data': u'Found 0 objects, expected 1.'}
            if (readjson['status'] == 0):
                login = readjson['data']['uid']
                print login
                r = requests.post(config['slack_url'],
                                  json={"text": config['slack_msg'] + login,
                                        "icon_emoji": config['slack_icon_emoji'],
                                        "username": config['slack_username']
                                        })
                print r.status_code
            else:
                print "unknown user"

