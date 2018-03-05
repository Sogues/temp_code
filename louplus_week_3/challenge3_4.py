# encoding: utf-8

import re
from datetime import datetime


def open_parser(filename):
    with open(filename) as logfile:

        pattern = (r''
                '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
                '\[(.+)\]\s'  # 时间
                '"GET\s(.+)\s\w+/.+"\s'  # 请求路径
                '(\d+)\s'  # 状态码
                '(\d+)\s'  # 数据大小
                '"(.+)"\s'  # 请求头
                '"(.+)"'  # 客户端信息
                )
        parsers = re.findall(pattern, logfile.read())

    return parsers

def main():
    parsers = open_parser('nginx.log')
    ip_dict = {}
    url_dict = {}
    for item in parsers:
        if "11/Jan/2017" in item[1]:
            if item[0] not in ip_dict.keys():
                ip_dict[item[0]] = 0
            ip_dict[item[0]] += 1
        if item[3] != '404':
            continue
        if item[2] not in url_dict.keys():
            url_dict[item[2]] = 0
        url_dict[item[2]] += 1
    ip_sort = sorted(ip_dict.items(), key=lambda X: X[1], reverse=True)
    url_sort = sorted(url_dict.items(), key=lambda X: X[1], reverse=True)
    ip_dict = {ip_sort[0][0]: ip_sort[0][-1]}
    url_dict = {url_sort[0][0]: url_sort[0][-1]}
    return ip_dict, url_dict

if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
