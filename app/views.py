from flask import render_template, flash, redirect
from app import app
from forms import LoginForm,RegistrationForm
import smtplib
from email.mime.text import MIMEText
import re
from mimetypes import guess_type
import envoy

from render_utils import make_context

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
    return render_template('index.html',
                   title = 'Home',
                   user = user,
                   posts = posts)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
            title = 'Sign in',
            form = form,
            providers = app.config['OPENID_PROVIDERS'],
            **make_context())

def send_mail(form):
    fp = open('reg_email.txt', 'rb')
    message = fp.read()
    re.sub('EMAIL', form.email.data, message)
    re.sub('INSTITUTION', form.institution.data, message)
    re.sub('MAJOR', form.major.data, message)
    re.sub('YEAR', form.year.data, message)
    re.sub('ABSTRACT_TITLE', form.abstracttitle.data, message)
    re.sub('ABSTRACT', form.abstract.data, message)
    re.sub('DISCIPLINE', form.discipline.data, message)

    msg = MIMEText(message)
    fp.close()

    msg['Subject'] = 'CAURS Registration'
    msg['From'] = 'me@example.com'
    msg['To'] = form.email.data

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    print 'hello world'
    if form.validate_on_submit():
        print 'hello world'
        send_mail(form)
        flash('stuff' + form.name.data)
        return redirect('/index')
    return render_template('register.html',
            title = 'Register',
            form = form,
            **make_context())

# Render LESS files on demand
@app.route('/less/<string:filename>')
def _less(filename):
  with open('less/%s' % filename) as f:
    less = f.read()

  r = envoy.run('node_modules/.bin/lessc -', data=less)
  return r.std_out, 200, { 'Content-Type': 'text/css' }

# Render JST files on demand
@app.route('/js/templates.js')
def _templates_js():
  r = envoy.run('node_modules/.bin/jst --template underscore jst')
  return r.std_out, 200, { 'Content-Type': 'application/javascript' }

# Serve arbitrary static files on demand
@app.route('/<path:path>')
def _img(path):
  with open('www/%s' % path) as f:
    return f.read(), 200, { 'Content-Type': guess_type(path)[0] }
