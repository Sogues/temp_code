# encoding: utf-8

import getopt
import sys
import re
import socket
import time


ip_pattern = '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
def judge_ip(ip):
    compile_ = re.compile(ip_pattern)
    if compile_.match(ip):
        return True;
    return False;

def judge_port(port):
    if '-' in port:
        port = port.split('-')
        if len(port) != 2:
            return None
        if port[0] > port[-1]:
            return None
        port = [item for item in range(int(port[0]), int(port[-1])+1)]
    else:
        port = [] + [port]
    return port




def parse(argv):
    config = {}
    try:
        opts, _ = getopt.getopt(argv, 'x',
                ['host=', 'port='])
        for key, value in opts:
            if key == '--host':
                if not judge_ip(key):
                    pass
                key = 'ip'
            elif key == '--port':
                port = judge_port(value)
                value = [int(p) for p in port]
                key = 'port'
            config[key] = value
        if 'ip' not in config.keys():
            raise Exception
        if 'port' not in config.keys():
            raise Exception
    except Exception as ex:
        print('Parameter Error')
        sys.exit(-1)
    print(config)
    return config

def deal_scan(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            s.connect((ip, port))
            return 1
    except Exception as ex:
        return 0


def main(argv):
    retcode = ['closed', 'open']
    config = parse(argv)
    for item in config.get('port', []):
        ret = deal_scan(config.get('ip'), item)
        print('{} {}'.format(item, retcode[ret]))

if __name__ == "__main__":
    main(sys.argv[1:])

