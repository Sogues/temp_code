from flask import Flask
from flask import render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@0.0.0.0/TEST'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))

    def __init__(self, title,  created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File(title=%s)>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category(name=%s)>' % self.name

root_dir = '/home/louplus/temp_code/louplus_week_2/files'

def get_data_from_json(filename):
    path = os.path.join(root_dir, filename)
    data = None
    with open(path, 'r') as f:
        data = json.load(f)
    return data



@app.route('/')
def index():
    config = []
    for filename in os.listdir(root_dir):
        data = get_data_from_json(filename)
        new_dict = {}
        new_dict['title'] = data['title']
        new_dict['url'] = url_for('file_from_json', filename=filename.split('.')[0])
        config.append(new_dict)
    print(config)
    return render_template('index.html', config=config)


@app.route('/file_from_json/<filename>')
def file_from_json(filename):
    flag = False
    for fn in os.listdir(root_dir):
        if filename  == fn.split('.')[0]:
            filename = fn
            flag = True
            break
    if flag is False:
        return render_template('404.html')
    else:
        data = get_data_from_json(filename)
        return render_template('file.html', data=data)

def get_data_from_tb(entry):
    data = {}
    data['title'] = entry.title
    data['created_time'] = entry.created_time
    data['category_name'] = entry.category.name
    data['content'] = entry.content
    return data


@app.route('/files/<file_id>')
def file(file_id):
    entry = db.session.query(File).filter(File.id == file_id).first()
    if entry is None:
        abort(404)
    data = get_data_from_tb(entry)
    return render_template('file.html', data=data)




@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.debug=1
    app.run(host='0.0.0.0', port=3000)
