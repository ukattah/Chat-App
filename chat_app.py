from flask import Flask, render_template, url_for, redirect, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}

db = SQLAlchemy(app)

# model for the user
class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
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
	author = db.Column(db.String(24), nullable=False)
	message = db.Column(db.String(200), nullable=False)

	def __init__(self, author, message):
		self.message = message
		self.author = author

	def to_dict(self):
		return {
    	"author": self.author,
        "message": self.message
     	}

	# tell Python how to print
	def __repr__(self):
		return '<Chat from {}>'.format(self.author)

# by default, direct to login
@app.route("/")
def default():
	return redirect(url_for("login_controller"))
	
@app.route("/login/", methods=["GET", "POST"])
def login_controller():
	if request.method == "POST":
		if "user" in request.form and "pass" in request.form:
			username = request.form["user"]
			password = request.form["pass"]
			user = User.query.filter_by(username=username).first()		  

			# check if a user exists and 
			# if the passwords match. 
			if user and user.password == password:  
				msgs = Chat.query.all()	# get all the messages in the chat.
				# render the template with the messages if there are any to display.
				render_template("chat_page.html", msgs=msgs)
				return redirect(url_for("profile", username=username))
			else:
				# return to the login page if no such user exists (get request)
				return redirect(url_for("login_controller"))	
	# get request.
	else:
   		return render_template("loginPage.html")
	
	    
@app.route("/profile/")
@app.route("/profile/<username>")
def profile(username=None):
	msgs = Chat.query.all()
	return render_template("chat_page.html", name=username, msgs=msgs)

@app.route("/register/", methods=["GET", "POST"])
def register_controller():
	if request.method == "POST":
		username = request.form["user"]
		password = request.form["pass"]
		email = request.form["email"]
		retyped_password = request.form["retyped_pass"]
		# check if all fields are filled. 
		if all([username, password, retyped_password, email]):
			# check if the passwords match.
			if password == retyped_password:
				# create a user.
				new_user = User(username=username, password=password, email=email)
				try:
					db.session.add(new_user)
					db.session.commit()
					return redirect(url_for("profile", username=username))
				except:
					return 'There was an issue adding your task'
			else:
				print("Passwords did not match. Try again.")
				return redirect(url_for("register_controller"))
	# get request. 
	return render_template("register.html")

@app.route("/logout/")
def unlogger():
	# if logged in, log out, otherwise offer to log in
	return redirect(url_for("login_controller"))
	
@app.route("/new_message/", methods=["POST"])
def new_message():
	message = request.form["message"]
	author = request.form["author"]
	# check if the author and message are obtainable. 
	new_msg = Chat(message=message, author=author)
	db.session.add(new_msg)
	db.session.commit()
	
	msgs = Chat.query.all()
	msgsArray = []
	for msg in msgs:
		msgsArray.append([msg.author, msg.message])
	return json.dumps(msgsArray)	# return "Missing message or author field", 400

@app.route("/messages/")
def messages():
	msgs = Chat.query.all()
	msgArr = []

	for msg in msgs:
		msgArr.append([msg.author, msg.message])
	return json.dumps(msgArr)

			
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

