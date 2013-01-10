from flask import render_template, flash, redirect
from app import app 
from app.database import db_session
from forms import LoginForm,RegistrationForm
from app.models import Presenters


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

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
            providers = app.config['OPENID_PROVIDERS'])

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
    p = Presenters(arg_dict=register_dict)
    db_session.add(p)
    db_session.commit()

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        handle_form_data(form_to_dict(form))
        flash('stuff' + form.name.data)
        return redirect('/index')
    return render_template('register.html',
            title = 'Register',
            form = form)

