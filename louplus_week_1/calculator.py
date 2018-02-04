#!/usr/bin/env python3

import sys


class ArgParse():
    def __init__(self, argv):
        self._argv = argv
        self.params = {}
        key, val = None, None
        for elem in argv:
            if (elem == '-c' or
                    elem == '-d' or
                    elem == '-o'):
                key = elem
            elif key == None:
                print('Parameter Error')
                #print('Parameter Error', sys._getframe().f_lineno)
                sys.exit(-1)
            elif key in self.params.keys():
                print('Parameter Error')
                #print('Parameter Error', sys._getframe().f_lineno)
                sys.exit(-1)
            else:
                self.params[key] = elem
                key = None
    def get_config_file(self):
        return self.params['-c']
    def get_data_file(self):
        return self.params['-d']
    def get_output_file(self):
        return self.params['-o']


def parse_config_file(filename):
    ret = {}
    with open(filename, 'r') as f:
        for elem in f.readlines():
            if (elem == '\n'): continue
            elem = elem.split('\n')[0]
            _tmp = elem.split(' ')
            try:
                ret[_tmp[0]] = float(_tmp[-1])
                if float(_tmp[-1]) < 0:
                    raise Exception
            except Exception as ex:
                print('Parameter Error')
                #print('Parameter Error', sys._getframe().f_lineno)
                f.close()
                sys.exit(-1)
    return ret

def parse_data_file(filename):
    ret = {}
    with open(filename, 'r') as f:
        for elem in f.readlines():
            if (elem == '\n'): continue
            elem = elem.split('\n')[0]
            _tmp = elem.split(',')
            try:
                ret[_tmp[0]] = int(_tmp[-1])
                if int(_tmp[-1]) < 0:
                    raise Exception
            except Exception as ex:
                print('Parameter Error')
                #print('Parameter Error', sys._getframe().f_lineno)
                f.close()
                sys.exit(-1)
    return ret


class calc():
    def __init__(self, config):
        try:
            self._jishul = config.pop('JiShuL')
            self._jishuh = config.pop('JiShuH')
        except Exception as ex:
            print('Parameter Error')
            #print(ex)
            #print('Parameter Error', sys._getframe().f_lineno)
            sys.exit(-1)
        self.rates = 0.0
        for key, val in config.items():
            self.rates += val

    def get_salary_pre(self, value):
        if value < self._jishul:
            value = self._jishul
        elif value > self._jishuh:
            value = self._jishuh
        return value

    def get_shebao(self, value):
        return self.get_salary_pre(value) * self.rates

    def get_geshui(self, value):
        sb = self.get_shebao(value)
        val = value - sb - 3500
        if val <= 0:
            val = 0.00
        elif val <= 1500:
            val = val * 0.03
        elif val <= 4500:
            val = val * 0.10 - 105
        elif val <= 9000:
            val = val * 0.20 - 555
        elif val <= 35000:
            val = val * 0.25 - 1005
        elif val <= 55000:
            val = val * 0.30 - 2755
        elif val <= 80000:
            val = val * 0.35 - 5505
        else:
            val = val * 0.45 - 13505
        _salary = value - sb - val
        if _salary <= 0:
            _salary = 0
        return [('%.2f'%sb),
                ('%.2f'%val),
                ('%.2f'%(_salary))]

def main(argv):
    if len(argv) != 7:
        print('Parameter Error')
        #print('Parameter Error', sys._getframe().f_lineno)
        return
    args = ArgParse(argv[1:])
    config = parse_config_file(args.get_config_file())
    calculator = calc(config)
    users = parse_data_file(args.get_data_file())
    ret = []
    for key, value in users.items():
        _tmp = [key, value]
        _tmp.extend(calculator.get_geshui(value))
        ret.append(_tmp)
    import csv
    with open(args.get_output_file(), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(ret)




if __name__ == '__main__':
    import time
    a = time.time()
    main(sys.argv)
    print(time.time() - a)
