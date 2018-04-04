#!/home/louplus/env/bin python
# encoding: utf-8

from flask import Blueprint, render_template
from simpledu.models import Course, User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def user_index(username):
    get_user = User.query.filter_by(username=username).first()
    if get_user is None:
        return "404"
    user_id = get_user.id
    courses = Course.query.filter_by(author_id=user_id).all()
    return render_template('user.html',
            id=user_id, username=username, courses=courses)


