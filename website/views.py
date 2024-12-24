from flask import Blueprint, render_template, request, flash, jsonify, Response, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from .models import Note, User, Img, MessangerDB, News
from . import db
import json

from werkzeug.utils import secure_filename

from flask_mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from werkzeug.security import generate_password_hash

from sqlite3 import OperationalError


views = Blueprint('views', __name__)


import base64



from flask_login import login_user, login_required, logout_user, current_user


@views.route('/test')
@login_required
def test():
    return render_template("bos.html", user=current_user)

@views.route('/')
@login_required
def home():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        return render_template("index.html", user=current_user, images=base64_images)
    else:
        return redirect(url_for('auth.logout'))

@views.route('/metaverse')
@login_required
def metaverse():
    if "user" in session:
        user = session["user"]
        return render_template("Metaverse/threejs-metaverse/src/index.html", user=current_user)
    else:
        return redirect(url_for('auth.logout'))

@views.route('/forum', methods = ['GET','POST'])
@login_required
def forum():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []
        for member in User.query.all():
            User_list.append(member)
        return render_template("forum.html", user=current_user, images=base64_images, members=User_list)
    else:
        return redirect(url_for('auth.logout'))


@views.route('/news', methods = ['GET','POST'])
@login_required
def news():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []
        for member in User.query.all():
            User_list.append(member)
        index_admin = 0
        index_user = 0
        
        
        if request.method == "POST":
            
            if current_user.is_admin == True:
                create_new_content = request.form.get('CNC')
                edit_existing_content = request.form.get('EEC')
                view_statistics = request.form.get('VS')
                rac = request.form.get('RAC')
                index_admin = 0
                
                
                if create_new_content:
                    
                    print("Redirecting to General create_new_content... ->")
                    return redirect(url_for('views.cnc'))

                    
                if edit_existing_content:
                    return redirect(url_for('views.eec'))
                    print("Redirecting to General edit_existing_content... ->")
                if view_statistics:
                    index_admin = 3
                    print("Redirecting to General view_statistics... ->")
                if rac:
                    index_admin = 4
                    print("Redirecting to rac... ->")
            else:
                general = request.form.get('G')
                muontech = request.form.get('MT')
                medical = request.form.get('M')
                cs = request.form.get('CS')
                ee = request.form.get('EE')
                rap = request.form.get('RAP')
                index_user = 0

                
                if general:
                    index_user = 1
                    print("Redirecting to general News... ->")
                if muontech:
                    index_user = 2
                    print("Redirecting to muontech News... ->")
                if medical:
                    index_user = 3
                    print("Redirecting to medical News... ->")
                if cs:
                    index_user = 4
                    print("Redirecting to cs News... ->")
                if ee:
                    index_user = 5
                    print("Redirecting to ee News... ->")
                if rap:
                    index_user = 6
                    print("Redirecting to rap News... ->")

        return render_template("news.html", user=current_user, images=base64_images, members=User_list, admin_cond=index_admin, user_cond=index_user)
    else:
        return redirect(url_for('auth.logout'))


@views.route('/create_new_content', methods = ['GET','POST'])
@login_required
def cnc():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []
        for member in User.query.all():
            User_list.append(member)
        index_admin = 1
        index_user = 0
        
        

        if current_user.is_admin == False:
            return redirect(url_for('views.news'))
        else:

            create_new_content = request.form.get('CNC')
            edit_existing_content = request.form.get('EEC')
            view_statistics = request.form.get('VS')
            rac = request.form.get('RAC')
            if create_new_content:
                index_admin = 1
                print("Redirecting to General edit_existing_content... ->")
                return redirect(url_for('views.cnc'))
            if edit_existing_content:
                index_admin = 2
                print("Redirecting to General edit_existing_content... ->")
                return redirect(url_for('views.eec'))
            if view_statistics:
                index_admin = 3
                print("Redirecting to General view_statistics... ->")
            if rac:
                index_admin = 4
                print("Redirecting to rac... ->")

            title_return = request.form.get('title-input')
            specid_return = request.form.get('specid-input')
            content_return = request.form.get('content-input')
            if request.method == "POST":
                title_return = request.form.get('title-input')
                specid_return = request.form.get('specid-input')
                content_return = request.form.get('content-input')
                if (len(specid_return) == 1) and (len(title_return) > 2) and (len(content_return) > 10):
                    print("OK")
                    new_post = News(spec_id=specid_return,admin_username=current_user.username,title=title_return,content=content_return)
                    db.session.add(new_post)
                    db.session.commit()
                    print(f'POST IS CREATED BY { current_user.username }')
                else:
                    print("IT IS NOT A VALID POST")
                    a = News.query.filter_by(admin_username=current_user.id).first()
                    if a:
                        print(a.title + a.content)
                
                
                    
                    
                
                

        return render_template("news.html", user=current_user, images=base64_images, members=User_list, admin_cond=index_admin, user_cond=index_user, title1=title_return, spcid=specid_return, content=content_return)
    else:
        return redirect(url_for('auth.logout'))

@views.route('/edit_existing_content', methods = ['GET','POST'])
@login_required
def eec():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []
        for member in User.query.all():
            User_list.append(member)
        index_admin = 2
        index_user = 0
        
        index_edit = 0

        content_edit = None

        if current_user.is_admin == False:
            return redirect(url_for('views.news'))
        else:
            create_new_content = request.form.get('CNC')
            edit_existing_content = request.form.get('EEC')
            view_statistics = request.form.get('VS')
            rac = request.form.get('RAC')
                    
            if create_new_content:
                index_admin = 1
                print("Redirecting to General edit_existing_content... ->")
                return redirect(url_for('views.cnc'))
            if view_statistics:
                index_admin = 3
                print("Redirecting to General view_statistics... ->")
            if rac:
                index_admin = 4
                print("Redirecting to rac... ->")

            title_return = request.form.get('title-input')
            specid_return = request.form.get('specid-input')
            admin_id_return = request.form.get('admin_id_return')
            if request.method == "POST":
                title_return = request.form.get('title-input')
                specid_return = request.form.get('specid-input')
                admin_id_return = request.form.get('admin_id_return')

                editara = News.query.filter_by(title=title_return,spec_id=specid_return,admin_username=admin_id_return).first()

                if editara:
                    print("FOUND THE CONTENT")
                    content_edit = editara.content
                    
                    return redirect(url_for('views.eec2', id=editara.id))
                    
                else:
                    print("NOT FOUND")

        

                
                
                

        return render_template("news.html", user=current_user, images=base64_images, members=User_list, edit_content=content_edit , admin_cond=index_admin, user_cond=index_user, title1=title_return, spcid=specid_return, adminid=admin_id_return, edit=index_edit)
    else:
        return redirect(url_for('auth.logout'))


@views.route('/edit_existing_content2/<id>', methods = ['GET','POST'])
@login_required
def eec2(id):
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []
        for member in User.query.all():
            User_list.append(member)
        index_admin = 2
        index_user = 0
        
        index_edit = 1

        

        editara = News.query.filter_by(id=id).first()

        if not editara:
            return redirect(url_for('views.news'))
        if current_user.is_admin == False:
            return redirect(url_for('views.news'))
        else:
            create_new_content = request.form.get('CNC')
            edit_existing_content = request.form.get('EEC')
            view_statistics = request.form.get('VS')
            rac = request.form.get('RAC')
                    
            if create_new_content:
                index_admin = 1
                print("Redirecting to General edit_existing_content... ->")
                return redirect(url_for('views.cnc'))
            if view_statistics:
                index_admin = 3
                print("Redirecting to General view_statistics... ->")
            if rac:
                index_admin = 4
                print("Redirecting to rac... ->")

            


            title_return = editara.title
            specid_return = editara.spec_id
            admin_id_return = editara.admin_username
            content_edit = editara.content
            if request.method == "POST":

                a = request.form.get('content-input')
                if (a != None) or (a != "None"):
                    editara.content = a
                    db.session.commit()
                    return redirect(url_for('views.news'))


        return render_template("news.html", user=current_user, images=base64_images, members=User_list, edit_content=content_edit , admin_cond=index_admin, user_cond=index_user, title1=title_return, spcid=specid_return, adminid=admin_id_return, edit=index_edit)
    else:
        return redirect(url_for('auth.logout'))

@views.route('/friends', methods=['GET', 'POST'])
@login_required
def friendship():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        
        main_acc = User.query.filter_by(id=current_user.id).first()


        ######### INCOMING LISTS ##########
        friend_list_text = main_acc.friends
        friend_sent_text = main_acc.friend_sent
        friend_pending_text = main_acc.friend_pending
        ###################################
        fl_SArr = friend_list_text.split("@")
        fs_SArr = friend_sent_text.split("@")
        fp_SArr = friend_pending_text.split("@")
        #print(fl_SArr)
        #print(fs_SArr)
        #print(fp_SArr)


        ###################################
        ####### USER ARRAYS #############
        ###################################
        fl_UArr = []
        fs_UArr = []
        fp_UArr = []
        ###################################
        ###################################
        for user in User.query.all():
            if user.username in fl_SArr:
                fl_UArr.append(user)
                print("USER ADDED")
            if user.username in fs_SArr:
                fs_UArr.append(user)
                print("USER ADDED TO SENT LIST")
            if user.username in fp_SArr:
                fp_UArr.append(user)
                print("USER ADDED TO PENDING LIST")
        ####################################


        #friend_list_text_test = "wertux@canbora@eternity@cafe@king221"
        #myArr = friend_list_text_test.split("@")
        #print(fl_UArr)
        #print(fs_UArr)
        #print(fp_UArr)

        if request.method == "POST":
            pass


        return render_template("friends.html", user=current_user, images=base64_images, friends=fl_UArr, sents=fs_UArr, pendings=fp_UArr)
    else:
        return redirect(url_for('auth.logout'))
    

def create_room_properties(user1, user2):

    username1 = user1.username
    
    username2 = user2.username
    
    Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    
    parse1 = str(username1.upper())
    username1_id = 0
    parse2 = str(username2.upper())
    username2_id = 0

    index1 = parse1[:1]
    index2 = parse2[:1]
    
    



    x =0
    for i in Alphabet:
        x+=1
        if i == index1:
            username1_id = x
        if i == index2:
            username2_id = x

    if username1_id < username2_id:
        return str(index1) + str(index2), str(user1.id) + str(user2.id)
    else:
        return str(index2) + str(index1), str(user2.id) + str(user1.id)
    print(room_id, type(room_id))
    

@views.route('/msn/<qmsnusername>', methods=(['GET','POST']))
@login_required
def msnn(qmsnusername):
    if "user" in session:
        user = session["user"]


        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        User_list = []

        my_acc = User.query.filter_by(email=current_user.email).first()
        guest_acc = User.query.filter_by(username=qmsnusername).first()
        
        if qmsnusername == 'profile':
                return redirect(url_for('views.perfil'))
        if qmsnusername == 'Q&A':
                return redirect(url_for('views.forum'))
        if qmsnusername == 'PLAY!':
                return redirect(url_for('views.metaverse'))
        if qmsnusername == 'logout':
            current_user.stat = False
            db.session.commit()
            logout_user()
            return redirect(url_for('auth.login'))
        if not guest_acc:
            #flash('You were successfully logged in')
            return redirect(url_for('views.home'))

       

        ####### CHAT ROOM PROPS #######
        letter_code, mixed_id = create_room_properties(my_acc, guest_acc)
        print(letter_code, mixed_id)

        chat_signiture = str(letter_code) + str(mixed_id)

        

        chat_room = MessangerDB.query.filter_by(chat_id=mixed_id).first()
        if chat_room:
            db_message = chat_room.messages
        if not chat_room:
            new_chat_db = MessangerDB(chat_id=mixed_id, chat_name=chat_signiture ,member=letter_code)
            
            db.session.add(new_chat_db)
            db.session.commit()
        else:
            if request.method == "POST":
                
                message = request.form.get('msn-input')
                if message:
                    message = str(my_acc.username) + " :" + " " + message + " " + "ß"
                    chat_room.messages = str(chat_room.messages) + " " + message
                    db_message = chat_room.messages
                    db.session.commit()



        
        return render_template("msn.html", members=User.query.all(), user=current_user, msnuser=qmsnusername,images=base64_images, message1=db_message )
    else:
        return redirect(url_for('auth.logout'))

@views.route('/friend', methods=['GET','POST'])
@login_required
def add_friend():
    
    
    return "FRIEND ADDED"


@views.route('/change_email/<token>')
@login_required
def change_email(token):
    with current_app.app_context():
        try:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            newemail = s.loads(token, salt="email-change")
            print(newemail)
            print(newemail)
            user = User.query.filter_by(email=current_user.email).first()
            user.email = newemail
            db.session.commit()
            #login_user(user, remember=True)
            print('New Email :' + user.email)
        except SignatureExpired:
            return 'The token is expired!'
    
    return render_template('email-confirmed.html', user=current_user)

@views.route('/profile/<user_name>', methods = ['GET','POST'])
@login_required
def perfilz(user_name):
    if "user" in session:
        user = session["user"]

        mem_list = []
        for member in User.query.all():
            mem_list.append(member.username)


        primero_nombre = user_name

        if primero_nombre == 'profile':
                return redirect(url_for('views.perfil'))
        if primero_nombre == 'Q&A':
                return redirect(url_for('views.forum'))
        if primero_nombre == 'PLAY!':
                return redirect(url_for('views.metaverse'))
        if primero_nombre == 'logout':
            current_user.stat = False
            db.session.commit()
            logout_user()
            return redirect(url_for('auth.login'))
        if primero_nombre in mem_list:
            
            if (primero_nombre != None or " "):
                main_acc = User.query.filter_by(username=current_user.username).first()
                usario = User.query.filter_by(username=primero_nombre).first()
                print(usario.friends)
                print(main_acc.friends)

                
                if usario:
                    main_acc_img = Img.query.filter_by(user_id=main_acc.id).first()
                    base64_main_acc = base64.b64encode(main_acc_img.p_image).decode("utf-8")
                    usario_img = Img.query.filter_by(user_id=usario.id).first()
                    base64_usario = base64.b64encode(usario_img.p_image).decode("utf-8")    
                else:
                    return "ERROR: NOT FOUND"
            if request.method == 'POST':
                
                message = request.form.get('friend_addition')

                message2 = request.form.get('friend_addition2')

                #CHECK IF THEY ARE FRIENDS
                if (main_acc.username in usario.friends) and (usario.username in main_acc.friends):
                    add_friend_button_condition = 0
                else:
                    add_friend_button_condition = 1

                if message2:
                    fm1 = str(main_acc.friends)
                    fm2 = fm1[fm1.startswith(f'@{primero_nombre}') and len(f'@{primero_nombre}'):]
                    main_acc.friends = fm2

                    fu1 = str(usario.friends)
                    fu2 = fu1[fu1.startswith(f'@{main_acc.username}') and len(f'@{main_acc.username}'):]
                    usario.friends = fu2

                    db.session.commit()

                    print("Removed Successfully..")

                    return redirect(url_for('views.friendship'))

                if message:

                    main_acc = User.query.filter_by(username=current_user.username).first()
                    usario = User.query.filter_by(username=primero_nombre).first()
                    if (primero_nombre in main_acc.friend_sent) or (main_acc.username in usario.friend_pending):
                        
                        
                        if (primero_nombre in main_acc.friend_sent) and (primero_nombre in main_acc.friend_pending):
                            print("Both sent friend request. Removing Sents and adding as friends both...")
                            print("Step 1: Accessing DB..")
                            print("Step 2: Trying to update Columns..")
                            formatted_nombre = "@" + primero_nombre
                            formatted_username = "@" + main_acc.username
                            
                            fsm1 = str(main_acc.friend_sent)
                            fsm2 = fsm1[fsm1.startswith(f'@{primero_nombre}') and len(f'@{primero_nombre}'):]
                            main_acc.friend_sent = fsm2
                            print(main_acc.friend_sent)

                            fsu1 = str(usario.friend_sent)
                            fsu2 = fsu1[fsu1.startswith(f'@{main_acc.username}') and len(f'@{main_acc.username}'):]
                            usario.friend_sent = fsu2
                            print(usario.friend_sent)

                            fpm1 = str(main_acc.friend_pending)
                            fpm2 = fpm1[fpm1.startswith(f'@{primero_nombre}') and len(f'@{primero_nombre}'):]
                            main_acc.friend_pending = fpm2
                            print(main_acc.friend_pending)

                            fpu1 = str(usario.friend_pending)
                            fpu2 = fpu1[fpu1.startswith(f'@{main_acc.username}') and len(f'@{main_acc.username}'):]
                            usario.friend_pending = fpu2
                            print(usario.friend_pending)

                            


                            print("Q-Debugger: If you saw this message, there is nothing happened extraordinary to malfunction...")
                            print("Step 3: Updating Friend Lists..")
                            main_acc.friends += "@" + primero_nombre
                            usario.friends += "@" + main_acc.username
                            db.session.commit()
                            print("Step 4: Saving database changes..")
                            print("Final Step: Redirectiong to Friend Manager...")
                            return redirect(url_for('views.friendship'))
                        else:
                            print("ALREADY SENT, NOTHING CAN BE MADE FURTHER!")
                            return redirect(url_for('views.friendship'))


                    else:
                        main_acc.friend_sent += "@" + primero_nombre
                        usario.friend_pending += "@" + main_acc.username
                        db.session.commit()
                        print(main_acc.friend_sent)
                        print(usario.friend_pending)
                        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

                        return redirect(url_for('views.friendship')) 
        else:
            return redirect(url_for('views.forum'))

        
        return render_template("perfilotro.html", user=usario, c_user=current_user, usario_images=base64_usario, images=base64_main_acc, member_username=primero_nombre, fcond=add_friend_button_condition)
    else:
        return redirect(url_for('auth.logout'))

@views.route('/profile', methods = ['GET','POST'])
@login_required
def perfil():
    if "user" in session:
        user = session["user"]
        
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        
        
        if request.method == 'POST':
            message1 = request.form.get("friend_redirect")
            message2 = request.form.get("perfil_settings")

            if message1:
                return redirect(url_for('views.friendship'))
            if message2:
                return redirect(url_for('views.perfil_change'))

            #return redirect(url_for('views.perfil_change'))

        return render_template("perfil.html", user=current_user, images=base64_images)

    else:
        return redirect(url_for('auth.logout'))

@views.route('/profile_settings', methods = ['GET','POST'])
@login_required
def perfil_change():
    if "user" in session:
        user = session["user"]
        img = Img.query.filter_by(user_id=current_user.id).first()
        base64_images = base64.b64encode(img.p_image).decode("utf-8")
        if request.method == 'POST':
            pic = request.files['pic']
            newemail = request.form.get('email')

            newpassword = request.form.get('password')

            print("E :" + newemail)
            print("P :" + newpassword)

            index1 = 0
            index2 = 0 
            index3 = 0 

            if (newemail and index2==0 and index3==0):
                index1 = 1
                index2 = 0
                index3 = 0
                with current_app.app_context():
                    try:
                        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                        token = s.dumps(newemail, salt="email-change")
                        mail = Mail(current_app)
                        msg = Message('Change Email', sender='casiquanta@gmail.com', recipients=[newemail])
                        link = url_for('views.change_email', token=token, _external=True)
                        msg.body = 'Your requested email change link is {}'.format(link)
                        mail.send(msg)
                        return redirect(url_for('e_mail'))
                        index1 = 0
                    except SignatureExpired:
                        return 'The token is expired!'
    

            if (newpassword and index1==0 and index3==0):
                index1 = 0
                index2 = 1
                index3 = 0
                user = User.query.filter_by(email=current_user.email).first()
                user.password = generate_password_hash(newpassword, method='sha256')
                db.session.commit()
                index2=0

            if (pic and index1==0 and index2==0):
                index1 = 0
                index2 = 0
                index3 = 1
                filename = secure_filename(pic.filename)
                mimetype = pic.mimetype
                
                
                
                img = Img.query.filter_by(user_id=current_user.id).first()
                img.p_image = pic.read()
                img.p_image_type = mimetype
                img.p_name = filename
                
                db.session.commit()

            
                #return redirect(url_for('views.image'))

                
                base64_images = base64.b64encode(img.p_image).decode("utf-8")

                return render_template('perfil_change.html', user=current_user,images=base64_images)
                index3 = 0


            

        

        return render_template("perfil_change.html", user=current_user, images=base64_images)

    else:
        return redirect(url_for('auth.logout'))


@views.route('/image')
def image():
    
    img = Img.query.filter_by(user_id=current_user.id).first()
    
    if not img:
        return 'No img found with that id', 404
        
    return Response(img.p_image, mimetype=img.p_image_type)


