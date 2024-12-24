from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import sqlalchemy


from PIL import Image
import io

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class News(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	spec_id = db.Column(db.Integer, nullable = False)
	admin_username = db.Column(db.String, default="Unknown", nullable=False)
	title = db.Column(db.String, default='Title', nullable= False)
	content = db.Column(db.Text, default=None)

	

class MessangerDB(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	chat_id = db.Column(db.Integer, unique=True)
	chat_name = db.Column(db.Text, unique=True, nullable=False)
	member = db.Column(db.Text(40), nullable=False)
	messages = db.Column(db.Text, default='<br>',nullable=False)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	is_admin = db.Column(db.Boolean, default=False, nullable=False)
	email = db.Column(db.String(150), unique=True)
	username = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	e_confirm = db.Column(db.Boolean, default=False, nullable=False)
	
	stat = db.Column(db.Boolean, default=False, nullable=False)

	friends = db.Column(db.Text, default="", nullable=False)
	friend_sent = db.Column(db.Text, default="", nullable=False)
	friend_pending = db.Column(db.Text, default="", nullable=False)

	
	image = db.relationship('Img')	
	notes = db.relationship('Note')


	


class Img(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	p_image = db.Column(db.LargeBinary, default=bytes([115, 112, 97, 109, 33]), nullable=False)
	p_name = db.Column(db.Text, default='default_pp',nullable=False)
	p_image_type = db.Column(db.Text, default='jpg',nullable=False)
	

	def load_default_image():
		im = Image.open(r"/home/webserver/website/static/assets/img/officialpp.jpg") 
		#im = Image.open('test.jpg')
		im_resize = im.resize((300, 300))
		buf = io.BytesIO()
		im_resize.save(buf, format='JPEG')
		byte_im = buf.getvalue()
		return byte_im
