from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from .models import User, Img
from werkzeug.security import check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


from flask_mail import Mail, Message



auth = Blueprint('auth', __name__)


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



@auth.route('/login', methods=['GET', 'POST'])
def login():
    remote_IP = request.remote_addr
    banned_list(remote_IP, 1)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        

        if user:
            
            if (check_password_hash(user.password, password)):
                if user.e_confirm == True:
                    try:
                        img = Img.query.filter_by(user_id=user.id).first()
                        print(img.user_id)
                    except AttributeError:
                        new_img = Img(user_id=user.id,p_image=Img.load_default_image())
                        db.session.add(new_img)
                        db.session.commit()
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    user.stat = True
                    db.session.commit()
                    session.permanent = True
                    session["user"] = user.username
                    return redirect(url_for('views.home'))
            else:
                print('Incorrect password, try again.')
                flash('Incorrect password, try again.', category='error')
        else:
            print("Email does not exist...")
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    current_user.stat = False
    session.pop("user", None)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))





