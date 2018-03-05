# encoding: utf-8

import os
import sys

def challenge_10():
    try:
        os.system('sudo service mongodb restart')
    except Exception as ex:
        os.sysmtem('sudo service mongod restart')

    state = 'wget http://labfile.oss.aliyuncs.com/courses/1013/week3/contests.json &&\
            mongoimport --db shiyanlou --collection contests --file ./contests.json --jsonArray '
    os.system(state)

def challenge_11():
    os.system('wget http://labfile.oss.aliyuncs.com/courses/1013/week3/courses.xlsx')

def main(arg):
    if arg == '10':
        challenge_10()
    elif arg == '11':
        challenge_11()


if __name__ == '__main__':
    main(sys.argv[1])
