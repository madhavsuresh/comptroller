from flask import render_template, flash, redirect
from app import app 
from app.database import db_session
from forms import LoginForm,RegistrationForm
from app.models import Presenters
from toolkit import handle_email, rand_gen
from mimetypes import guess_type
import envoy


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


from render_utils import make_context

@app.route('/')
@app.route('/index')
def index():
    return 'caurs!!'

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


def form_to_dict(form):
    ret = {}
    ret['name'] = form.name.data
    ret['email'] = form.email.data
    ret['institution'] = form.institution.data
    ret['major'] = form.major.data
    ret['year'] = form.year.data
    ret['abstract_title'] = form.abstract_title.data
    ret['discipline'] = form.discipline.data
    ret['abstract'] = form.abstract.data
    return ret

def handle_form_data(register_dict):
    reg_num = rand_gen()
    register_dict['reg_num'] = reg_num
    p = Presenters(arg_dict=register_dict)
    handle_email(register_dict['email'],register_dict)
    db_session.add(p)
    db_session.commit()


@app.route('/view/<regnum>',methods=['GET','POST'])
def get_by_regnum(regnum):
    row = Presenters.query.filter_by(reg_num = regnum).first()
    row_dict = dict((col, getattr(row, col)) for col in row.__table__.columns.keys())
    return render_template('viewreg.html',info = row_dict, **make_context())

    
    
    

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        handle_form_data(form_to_dict(form))
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
