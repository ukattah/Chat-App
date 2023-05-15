from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# model for the user
class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
	# tell Python how to print
	def __repr__(self):
		return '<User {}>'.format(self.username)

# model for chat
class Chat(db.Model):
	__bind_key__ = 'chat'
	chat_id = db.Column(db.Integer, primary_key=True)
	chat_name = db.Column(db.String(24), nullable=False, unique=True)

	def __init__(self, chat_name, creator_id):
		self.chat_name = chat_name
		self.creator_id = creator_id

	# tell Python how to print
	def __repr__(self):
		return '<Chat Name {}>'.format(self.chat_name)

# model for a message
class Message(db.Model):
	msg_id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(24), nullable=False)
	contents = db.Column(db.String(1024), nullable=False)
	chatroom = db.Column(db.Integer, nullable=False)
	
	def __init__(self, author, contents, chatroom):
		self.author = author
		self.contents = contents
		self.chatroom = chatroom
		
	def as_dict(self):
		return {'author': self.author, 'contents': self.contents}