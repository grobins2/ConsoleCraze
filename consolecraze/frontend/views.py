import simplejson as json
from flask import Blueprint, request, render_template, flash, g, session, \
        redirect, url_for, current_app, jsonify
from consolecraze.users.models import User

mod = Blueprint('frontend', __name__,)

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

def get_json_response(view_name, *args, **kwargs):
    view = current_app.view_functions[view_name]
    res = view(*args, **kwargs)
    js =  json.loads(res.data)
    return js

@mod.route("/")
def index():
    js = get_json_response('articles.all_articles')
    titles = [t['title'] for t in js['articles']]
    return render_template('frontend/index.html', articles=js['articles'],
            user=g.user)
