#!/usr/bin/env python
from flask import Flask, render_template, url_for, session, flash
from flask import make_response
from flask import redirect
from flask import abort
from flask.ext.script import Manager #or so from flask_script import Manager
from flask.ext.bootstrap import Bootstrap #or so from flask_bootstrap import Bootstrap
from flask.ext.moment import Moment #from flask_moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand



app=Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
app.config['SECRET_KEY']='hello world'



# @app.route('/index')
# def index():
#     return render_template('index.html', current_time=datetime.utcnow())

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     name=None
#     form=NameForm()
#     if form.validate_on_submit():
#         name=form.name.data
#         form.name.data=''
#     return render_template('index.html', form=form, name=name)    

# @app.route('/', methods=['GET', "POST"])
# def index():
#     form=NameForm()
#     if form.validate_on_submit():
#         session['name']=form.name.data
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'))    

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     form=NameForm()
#     if form.validate_on_submit():
#         old_name=session.get('name')
#         if old_name is not None and old_name!=form.name.data:
#             flash('Looks like you have changed your name')
#         session['name']=form.name.data
#         form.name.data=''
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'))    

@app.route('/', methods=['GET', 'POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))        

@app.route('/user/<user>')
def user(user):
    return render_template('user.html', name=user)

@app.route("/get")
def get_404():
    return "<h1>Bad Request </h1>", 400    

@app.route("/cookie")
def main():
    response=make_response("<h1>This document carries a cookie!</h1>")
    response.set_cookie('answer', '12')
    return response

@app.route('/redirect')
def redir():
    return redirect("/cookie")

@app.route("/get_err/<user>")
def get_err(user):
    if int(user)<100:
        abort(404)
    return "<h3>Hello user {}</h3>".format(user)    

@app.errorhandler(404)
def page_not_found(e):
    # print(type(url_for('main')))
    # url_name=url_for('main', _external=True)
    return render_template('404.html'), 404    

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



#configuration of database
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)

#models for database
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return "<Role {}>".format(self.name)

    users=db.relationship('User', backref='role', lazy='dynamic')    

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), index=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    role_id=db.Column(db.Integer, db.ForeignKey('roles.id'))    



#for forms
class NameForm(Form):
    name=StringField("What is your name?", validators=[Required()])
    submit=SubmitField("Submit")    



#for integration with shell of python 
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))    



#for migrate configuration
migrate=Migrate(app, db)
manager.add_command('db', MigrateCommand)



if __name__=="__main__":
    manager.run()









