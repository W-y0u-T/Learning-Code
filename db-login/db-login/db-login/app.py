"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, session, url_for, redirect, escape, render_template, request
import pymysql
from hashlib import md5
app=Flask(__name__)
app.secret_key="daniel deng is bad"
def display_all_records():
	global data
	connection=create_connection()
	try:
		with connection.cursor() as cursor:
			#comments
			select_sql= "SELECT tblusers.ID AS ID, tblusers.Email AS Email, tblusers.FirstName AS FirstName, tblusers.FamilyName AS FamilyName"
			if int(id)>0:
				print(select_sql)
				print(ID)
				select_sql = select_sql+"WHERE tblusers.ID="+ID
				val=int(ID)
				print(select_sql)
				cursor.execute(select_sql)
				data= cursor.fetchone()
				print(data)
			cursor.execute(select_sql)
			data=cursor.fetchall()
			data=list(data)
	finally:
		connection.close()

def create_connection():
    return pymysql.connect(host='localhost',
                             user='root',
                             password='13COM',
                             db='sampythondb',
                             charset='utf8mb4'
                             ,cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

class ServerError(Exception):
   """Base class for other exceptions"""
   pass
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
	if session.get('logged_in'):
		username_session=escape(session['username']).capitalize()
		return render_template("index.html", session_user_name=username_session)
	username_session=''
	return render_template("index.html")
#	connection=create_connection()
#	try:
#		with connection.cursor() as cursor:
#			sql = "SELECT * from users"
#			cursor.execute(sql)
#			data = cursor.fetchall()
#			data=list(data)
#	finally:
#			connection.close()
	return render_template("Index.html", results=data)

@app.route('/login', methods=["GET","POST"])
def login():
	connection=create_connection()
	if session.get('logged_in'):
		display_all_records()
		username_session=escape(session['username']).capitalise()
		return redirect(url_for('index.html', results = data, session_user_name=username_session))
	error=None
	try:
		with connection.cursor() as cursor:
			if request.method == "POST":
				username_form= request.form['username']
				select_sql='SELECT COUNT(1) FROM tblusers WHERE UserName = %s'
				val=(username_form)
				cursor.execute(select_sql,val)
				#data = cursor.fetchall()

				if not list(cursor.fetchone())[0]:
					raise ServerError('Invalid username')

				password_form = request.form['password']
				select_sql="SELECT Password FROM tblusers WHERE UserName = %s"
				val=(username_form)
				cursor.execute(select_sql,val)
				data = list(cursor.fetchall())
				print(data)
				for row in data:
					print(md5(password_form.encode()).hexdigest())
					if md5(password_form.encode()).hexdigest()==row["Password"]:
						session['username'] = request.form['username']
						session['logged_in'] = True
						return redirect(url_for('home'))

				raise ServerError('Invalid password')
	except ServerError as e:
		error = str(e)
		sesssion['logged_in']= False

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for("home"))
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
