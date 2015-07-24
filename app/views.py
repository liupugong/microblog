from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm, oid
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User

# index view function suppressed for brevity

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname','email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


def load_user(id):
    return User.query.get(int(id))


