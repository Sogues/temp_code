# encoding: utf-8

import sys
from pymongo import MongoClient


def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    infos = {}
    for entry in contests.find():
        tmp = infos.setdefault(str(entry['user_id']), {})
        tmp['scores'] = tmp.get('scores', 0) + entry['score']
        tmp['submit_time'] = tmp.get('submit_time', 0) + entry['submit_time']
        infos[str(entry['user_id'])].update(tmp)
    if user_id not in infos.keys():
        print('NOTFOUND')
        sys.exit(-1)
    def new_cmp(x, y):
        if x[1].get('scores', 0)  != y[1].get('scores', 0):
            return 1 if x[1].get('scores') > y[1].get('scores') else -1
        elif x[1].get('submit_time', 0) != y[1].get('submit_time', 0):
            return 1 if x[1].get('submit_time', 0) < y[1].get('submit_time', 0) else -1
        return 0
    import functools
    new_infos = sorted(infos.items(), key=functools.cmp_to_key(new_cmp), reverse=True)
    rank = 1
    for key, value in new_infos:
        if key == user_id:
            break
        rank += 1
    return rank, infos[user_id].get('scores', 0), infos[user_id].get('submit_time', 0)


if __name__ == '__main__':
    try:
        user_id = sys.argv[1]
    except Exception as ex:
        print('Parameter Error')
        sys.exit(-1)

    userdata = get_rank(user_id)
    print(userdata)
