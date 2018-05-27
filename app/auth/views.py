

from flask import render_template,redirect,url_for,request,flash
from . import auth
from ..models import User
from flask_login import login_user,logout_user,login_required
from .forms import RegistrationForm, LoginForm
from .. import db

# registration route
@auth.route('/reqister',methods=['GET','POST'])
def register():
    form =RegistrationForm()
    if form.validate_on_submit():
        user =User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
        title='Register your Account'
    return render_template('auth/register.html',registration_form=form)

    
# Login route
@auth.route('/login',methods=['GET','POST'])
def login():
    '''
    Function that checks if the form is validated
    '''
    login_form=LoginForm()
    if login_form.validate_on_submit():
        user=User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)

            # redirect the admin to the admin dashboard
            if user.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('./AdminDashboard'))
        else:
            flash('Invalid email or password,')

    title ="Time to Blog"
    return render_template('auth/login.html',login_form=login_form,title=title)

#logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))