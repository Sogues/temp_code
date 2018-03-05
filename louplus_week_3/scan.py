# encoding: utf-8

import getopt
import sys
import re


ip_pattern = '^(((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?))$'
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
    else:
        port = list(port)
    return port




def parse(argv):
    config = {}
    try:
        opts, _ = getopt.getopt(argv, 'x',
                ['host=', 'port='])
        for key, value in opts:
            if key == '--host':
                print(judge_ip(key))
                if not judge_ip(key):
                    pass
                key = 'ip'
            elif key == '--port':
                port = judge_port(value)
                value = [int(p) for p in port]
                key = 'port'
            config[key] = value
    except Exception as ex:
        print(ex)
        print('Parameter Error')
        sys.exit(-1)
    print(config)
    return config

def main(argv):
    config = parse(argv)

if __name__ == "__main__":
    main(sys.argv[1:])

