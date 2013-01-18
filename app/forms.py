from flask.ext.wtf import Form, TextField, BooleanField,SelectField,validators,TextAreaField,IntegerField,html5,RadioField
import constants

class LoginForm(Form):
    openid = TextField('openid', validators = [validators.required()])
    remember_me = BooleanField('remember_me', default = False)

schools = [('depaul','Depaul University'),('iit','Illinois Institute of Technology'),
        ('loyola','Loyola University Chicago'),('northwestern','Northwestern University'),
        ('uofc','University of Chicago'),('uic','University of Illinois at Chicago'),('other','Other')]
bio_sub = [('biochem_biophys','Biochemistry and Biophysics'),
        ('clinre','Clinical Research'),
                    ('cellgendev','Cellular/Molecular Biology, Genetics, and Developmental Biology'),
                    ('immmicroviro','Immunology/Microbiology/Virology'),
                    ('neuro','Neurosciences'),
                    ('compubio','Systems Biology/Computational Biology')]


class RegistrationForm(Form):
    fname = TextField('First Name', [validators.length(max=constants.MAX_NAME),validators.required()])
    lname = TextField('Last Name', [validators.length(max=constants.MAX_NAME),validators.required()])
    email = TextField('Email',[validators.length(max=constants.MAX_EMAIL),validators.required(),validators.email()])
    confirm_email = TextField('Confirm Email',[
                                                validators.required(), 
                                                validators.EqualTo('email',message='emails must match'),
                                                validators.email()
                                                ])
    institution = SelectField(u'Institution',[validators.required()],choices= schools)
    major = TextField('Major',[validators.required(),validators.length(max=constants.MAX_MAJOR)])
    year = IntegerField(u'Graduation Year',[validators.required()])
    abstract_title = TextField('Research Project Title',[validators.required(),validators.length(max=constants.MAX_TITLE)])
    discipline = TextField('Academic Discipline',[validators.required()])
    abstract = TextAreaField('Abstract',[validators.required()])
    bio_subfield = RadioField('Biological Science Subfield',choices= bio_sub)

