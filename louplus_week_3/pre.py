# encoding: utf-8

import os

def main():
    try:
        os.system('sudo service mongodb restart')
    except Exception as ex:
        os.sysmtem('sudo service mongod restart')

    state = 'wget http://labfile.oss.aliyuncs.com/courses/1013/week3/contests.json &&\
            mongoimport --db shiyanlou --collection contests --file ./contests.json --jsonArray '
    os.system(state)

if __name__ == '__main__':
    main()
