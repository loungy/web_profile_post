from flask import Blueprint, render_template, abort, current_app, Markup
from jinja2 import TemplateNotFound, Environment
import json
import time

web_page = Blueprint('web_page', __name__, static_folder='static', template_folder='templates')

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    local_time = time.localtime(value / 1000.0)
    return time.strftime(format, local_time)


def format_text(value, class_id='reg_14'):
    textList = value.splitlines()
    result = ""
    for text in textList:
        result += "<p class=%s>%s</p>" % (class_id, text)
    return Markup(result)


@web_page.route('/post/<post_id>')
def get_post(post_id):
    post_filename = 'webpage/test_data/post_%s' % post_id
    reply_filename = 'webpage/test_data/reply_%s' % post_id
    with open(post_filename, 'r') as f:
        post = json.loads(f.read())

    with open(reply_filename, 'r') as f:
        replies = json.loads(f.read())

    title = post["text"][:20]

    current_app.jinja_env.filters['loungydate'] = format_datetime
    current_app.jinja_env.filters['loungytext'] = format_text
    try:
        return render_template('board.html', post=post, replies=replies, title=title, text=post["text"])
    except TemplateNotFound:
        abort(404)


@web_page.route("/p/<user_id>")
def get_user_id(user_id):

    filename = 'webpage/test_data/profile_%s' % user_id

    with open(filename, 'r') as f:
        info = json.loads(f.read())

    company = info["company"]
    position = info["position"]

    current_app.jinja_env.filters['loungydate'] = format_datetime
    current_app.jinja_env.filters['loungytext'] = format_text
    try:
        return render_template('profile.html', profile=info, company=company, position=position)
    except TemplateNotFound:
        abort(404)