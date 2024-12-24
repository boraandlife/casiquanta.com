from website import *

import sys
import os

from flask import Flask, abort
from flask import current_app
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session

from flask_mail import Mail, Message

from flask_login import login_required, current_user
from flask_login import login_user, logout_user



from werkzeug.security import generate_password_hash

import json

from website.models import User, Img



from itsdangerous import URLSafeTimedSerializer, SignatureExpired



from datetime import timedelta

from logging import FileHandler,WARNING




######## APP #############
app = create_app()
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'casiquanta@gmail.com'
app.config['MAIL_PASSWORD'] = 'omzpitvrwotnalhj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=300)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

#app.permanent_session_lifetime = timedelta(seconds=10)
#app.config['SERVER_NAME'] = 'KOALA'
######## MAIL SETUP ######
mail = Mail(app)
######## TOKEN ############
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
###########################

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


carry = [""]

def set_database():
    db_list = []
    for user in User.query.all():
        db_list.append(str("Username: " + user.username + "  Email: " + user.email + "  E-Confirm: " + str(user.e_confirm) + "\n"))
    print(db_list)

    db_list_text = "".join(db_list)
    with open("./instance/db_users.txt","w") as f:
        f.write(db_list_text)


def login_error_handling():
    for user in User.query.all():
        if user.e_confirm == False and user.is_authenticated:
            print("Found Login Error, loging out user..")
            logout_user()

@app.before_request
def func():
  session.modified = True
  set_database()
  login_error_handling()


  


def carry_item(text, listc):
    listc[0] = text 


        
def banned_list(ip, cond):
    ip_list = []
    with open('./instance/ssi.txt',"r") as f:
        lines = f.read()
        ip_list = lines.split("@")
        if cond == 1:
            print(ip_list)
            if str(ip) in ip_list:
                abort(403)

            f.close()
    with open('./instance/ssi.txt',"a") as f:
        if cond == 2:
            f.write(str(ip) + "@")
            f.close()
            print("Banned conn : " + ip)
        else:
            print("No condition")
            f.close()


    

  



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    admin_list = ['bora.yavuzer@std.yeditepe.edu.tr', 'faker.hesap@gmail.com']
    remote_IP = request.remote_addr
    spam_words = ['Hello World','http','https', 'https://']

    proceed_bool = True

    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    

    
    banned_list(remote_IP, 1)
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        username = request.form.get('userName')
        email = request.form.get('email')
        token = s.dumps(email, salt="email-confirm")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        for word in spam_words:
            if word in first_name:
                print("Spam / hacker detected, aborting connection to the client")
                print("Printing first name : " + first_name)              
                proceed_bool = False
            if word in username:
                print("Spam / hacker detected, aborting connection to the client")
                print("Printing username : " + username)    
                proceed_bool = False


        
        if not proceed_bool:
            print("Banning : " + remote_IP)
            banned_list(remote_IP, 2)
        else:

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                email = request.form['email']
                token = s.dumps(email, salt="email-confirm")
                carry_item(email, carry)

                msg = Message('Confirm Email', sender='casiquanta@gmail.com', recipients=[email])
                link = url_for('confirm_email', token=token, _external=True)
                msg.body = 'Welcome to our society! Your activation link is {}'.format(link)
                mail.send(msg)
                if email in admin_list:
                    new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1), e_confirm=False, username=username, is_admin=True)
                else:
                    new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1), e_confirm=False, username=username)
                
                db.session.add(new_user)
                db.session.commit()
                new_img = Img(user_id=new_user.id,p_image=Img.load_default_image())
                db.session.add(new_img)
                db.session.commit()
                
                
                return redirect(url_for('e_mail'))

    return render_template("sign-up.html", user=current_user)


@app.route('/sent-email')
def e_mail():
    return render_template('email-sent.html', user=current_user)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)

        if current_user:
            current_user.stat = False
            db.session.commit()
            logout_user()
        
        user = User.query.filter_by(email=email).first()
        user.e_confirm = True
        user.stat = True
        db.session.commit()
        login_user(user, remember=True)
    except SignatureExpired: 
        try:
            print("Retrieving token, converting to text, deleting the user...")
            email_Exit = s.loads(token, salt='email-confirm')
            
            try:
                user = User.query.filter_by(email=email_Exit).first()
                if user:
                    user_img = Img.query.filter_by(user_id=user.id).first()
                    db.session.delete(user)
                    db.session.delete(user_img)
                    db.session.commit()
                    print("Inactive USER is Succesfully DELETED...")
                else:
                    print("User is already deleted..")
            except:
                print("Some Error rised up! ~2")
        except:
            print("Some Error rised up!")
        return abort(401)
        
    
    return render_template('email-confirmed.html', user=current_user)



def read_port():
    with open('./instance/pinfo.txt', 'r') as f:
        port = f.read()

    return str(port)



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=read_port(),debug=True, use_reloader=True)
