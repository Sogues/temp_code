# encoding: utf-8

from app import *
db.create_all()
db.session.query(File).delete()
db.session.query(Category).delete()
db.session.commit()

java = Category('Java')
python = Category('Python')
file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
db.session.add(java)
db.session.add(python)
db.session.add(file1)
db.session.add(file2)
db.session.commit()

file1.add_tag('tech')
file1.add_tag('java')
file1.add_tag('linux')
file2.add_tag('tech')
file2.add_tag('python')
