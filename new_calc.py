#!/usr/bin/env python3

import sys
from multiprocessing import Process, Queue

queue_1 = Queue()
queue_2 = Queue()


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

def handler_queue_over(data):
    if len(data) != 2:
        return False
    name, val = data
    if name == 'over' and val == -1:
        return True
    return False


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
                #ret[_tmp[0]] = int(_tmp[-1])
                if int(_tmp[-1]) < 0:
                    raise Exception
                queue_1.put((_tmp[0], int(_tmp[-1])))
            except Exception as ex:
                print('Parameter Error')
                #print('Parameter Error', sys._getframe().f_lineno)
                f.close()
                sys.exit(-1)

    queue_1.put(('over', -1))
    #return ret


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
            value = self.jishul
        elif value > self._jishuh:
            value = self.jishuh
        return value

    def get_shebao(self, value):
        return self.get_salary_pre(value) * self.rates

    def get_geshui(self):
        while 1:
            data = queue_1.get()
            name, value = data
            if handler_queue_over(data):
                break
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

            ret = [name, value,
                    ('%.2f'%sb),
                    ('%.2f'%val),
                    ('%.2f'%(value-sb-val))]
            queue_2.put(ret)
        queue_2.put(('over', -1))
        """
        return [('%.2f'%sb),
                ('%.2f'%val),
                ('%.2f'%(value-sb-val))]
        """

def handle_write(filename):
    import csv
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        while 1:
            data = queue_2.get()
            if handler_queue_over(data):
                break
            #print('handle_write', data)
            writer.writerow(data)

def main(argv):
    if len(argv) != 7:
        print('Parameter Error')
        #print('Parameter Error', sys._getframe().f_lineno)
        return
    args = ArgParse(argv[1:])
    config = parse_config_file(args.get_config_file())
    calculator = calc(config)

    data_pro = Process(target=parse_data_file, args=(args.get_data_file(),))
    calc_pro = Process(target=calculator.get_geshui)
    write_pro = Process(target=handle_write, args=(args.get_output_file(), ))

    data_pro.start()
    calc_pro.start()
    write_pro.start()
    """
    data_pro.join()
    calc_pro.join()
    write_pro.join()
    """


if __name__ == '__main__':
    main(sys.argv)
