from flask import Flask
from flask import render_template
import json
import os

app = Flask(__name__)

root_dir = '/home/louplus/temp_code/louplus_week_2/files'

def get_data(filename):
    path = os.path.join(root_dir, filename)
    data = None
    with open(path, 'r') as f:
        data = json.load(f)
    return data



@app.route('/')
def index():
    titles = []
    for filename in os.listdir(root_dir):
        data = get_data(filename)
        titles.append(data['title'])
    return render_template('index.html', titles=titles)



@app.route('/files/<filename>')
def file(filename):
    flag = False
    for fn in os.listdir(root_dir):
        if filename  == fn.split('.')[0]:
            filename = fn
            flag = True
            break
    if flag is False:
        return render_template('404.html')
    else:
        data = get_data(filename)
        return render_template('file.html', data=data)

if __name__ == '__main__':
    app.debug=0
    app.run(host='0.0.0.0', port=3000)
