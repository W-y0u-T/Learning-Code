"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, session, url_for, redirect, escape, render_template, request,abort
import pymysql, hashlib
from hashlib import md5
app=Flask(__name__)

app.secret_key="daniel deng is bad"
def display_all_records(role="admin",Id=0):
    global data
    connection=create_connection()
    try:
        with connection.cursor() as cursor:
          #pull records and display using a left join
          #select_sql = "SELECT * from users"
          #if role not "admin"
          select_sql= "SELECT tblusers.ID AS ID, tblusers.Email AS Email, tblusers.FirstName AS FirstName, tblusers.FamilyName AS FamilyName FROM tblusers"
          if int(Id)>0:
            print(select_sql)
            print (Id)
            select_sql = select_sql+" Where tblusers.ID="+Id
            val=(int(Id))
            print(select_sql)
            cursor.execute(select_sql)
            data = cursor.fetchone()
            print(data)
          cursor.execute(select_sql)
          data = cursor.fetchall()
          data=list(data)
    finally:
          connection.close()



class ServerError(Exception):pass


def create_connection():
    return pymysql.connect(host='localhost',
                             user='root',
                             password='13COM',
                             db='sampythondb',
                             charset='utf8mb4'
                             ,cursorclass=pymysql.cursors.DictCursor)


class ServerError(Exception):
   """Base class for other exceptions"""
   pass
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
	print(session.get('logged_in',"Not_Logged In"))
	if  session.get('logged_in'):
		print(session.get("username", "None Found"))
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

#login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#	connection=create_connection()
#	if  session.get('logged_in'):
#		display_all_records()
#		username_session=escape(session['username']).capitalize()
#		return redirect(url_for("index", results=data,session_user_name=username_session))
#	error = None
#	try:
#		with connection.cursor() as cursor:
#			if request.method == 'POST':
#				username_form  = request.form['username']
#				select_sql = "SELECT COUNT(1) FROM tblusers WHERE UserName = %s"
#				val =(username_form)
#				cursor.execute(select_sql,val)
#				#data = cursor.fetchall()

#			if not list(cursor.fetchone())[0]:
#				raise ServerError('Invalid username')

#			password_form  = request.form['password']
#			select_sql = "SELECT Password from tblusers WHERE UserName = %s"
#			val=(username_form)
#			cursor.execute(select_sql,val)
#			data = list(cursor.fetchall())
#			#print (data)
#			for row in data:
#				print(md5(password_form.encode()).hexdigest())
#				if md5(password_form.encode()).hexdigest()==row['Password']:
#					session['username'] = request.form['username']
#					print

#					session['logged_in'] = True
#					return redirect(url_for('home'))

#			raise ServerError('Invalid password')
#	except ServerError as e:
#		error = str(e)
#		session['logged_in']=False
		
#	return render_template('login.html', error=error)
# update from form

@app.route('/add_user', methods=['POST','GET'])
def new_user():
   connection=create_connection()
   if request.method == 'POST':
         form_values = request.form 
         first_name = form_values["firstname"]
         family_name = form_values["familyname"]
         email = form_values["email"]
         password = form_values["password"]
         password = hashlib.md5(password.encode()).hexdigest()
         dob=form_values=['dob']
         try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `tblusers` (FirstName,FamilyName,Email,Password) VALUES (%s,%s,%s,%s)"
                val=(first_name,family_name,email,password)
                cursor.execute(sql,(val))
                print('working')
                #save values in dbase
            connection.commit()
            cursor.close()
            with connection.cursor() as cursor:
                #pull records and display
                sql = "SELECT * from tblusers"
                cursor.execute(sql)
                data = cursor.fetchall()
                data=list(data)
         finally:
             connection.close()
         return redirect(url_for('users'))
   return render_template("add_user.html")

#users
@app.route('/users')
def users():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	else:
		username_session=escape(session['username']).capitalize()
		display_all_records("admin")
		print(data)
	return render_template("users.html",results = data, session_user_name=username_session)


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection=create_connection()
    if  session.get('logged_in'):
        display_all_records()
        username_session=escape(session['username']).capitalize()
        return redirect(url_for("index", results=data,session_user_name=username_session))
    error = None
    try:
        with connection.cursor() as cursor:
         if request.method == 'POST':
            username_form  = request.form['username']
            select_sql = "SELECT COUNT(1) FROM tblusers WHERE UserName = %s"
            val =(username_form)
            cursor.execute(select_sql,val)
            #data = cursor.fetchall()

            if not list(cursor.fetchone())[0]:
                raise ServerError('Invalid username')

            password_form  = request.form['password']
            select_sql = "SELECT Password from tblusers WHERE UserName = %s"
            val=(username_form)
            cursor.execute(select_sql,val)
            data = list(cursor.fetchall())
            #print (data)
            for row in data:
                #print(md5(password_form.encode()).hexdigest())
                if md5(password_form.encode()).hexdigest()==row['Password']:
                    session['username'] = request.form['username']
                    session['logged_in'] = True
                    return redirect(url_for('home'))

            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)
        session['logged_in']=False

    return render_template('login.html', error=error)

@app.route('/edit_user', methods=['POST','GET'])
def update_user():
	user_id = request.args.get('id')
	connection=create_connection()
	if request.method == 'POST':
			form_values = request.form 
			first_name = form_values.get("firstname")
			family_name = form_values.get("familyname")
			email = form_values.get("email")
			password = form_values.get("password")
			password = hashlib.md5(password.encode()).hexdigest()
			user_id = form_values.get('ID')
			try:
				with connection.cursor() as cursor:
					# Create a new record
					sql = "UPDATE `tblusers` SET FirstName=%s,FamilyName=%s,Email=%s,Password=%s WHERE ID=%s"
					val=(first_name,family_name,email,password, user_id)
					cursor.execute(sql,(val))
					data = cursor.fetchall()
					data=list(data)
					#save values in dbase
				connection.commit()
				cursor.close()
			finally:
				connection.close()
			return redirect(url_for('users'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from tblusers where ID=%s"
			cursor.execute(sql, user_id)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("Edit_record.html",data=data)

@app.route('/delete_user', methods =["GET","POST"])
def delete_record():
	user_ID = request.args.get("id")
	connection=create_connection()
	if request.method == "POST":
		form = request.form
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "DELETE FROM  `tblusers` WHERE ID = %s "
				val=(user_ID)
				cursor.execute(sql,(val))
				data = cursor.fetchall()
				data=list(data)
			#save values in dbase
			connection.commit()
			cursor.close()
		finally:
			connection.close()
			return redirect(url_for('users'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from tblusers where ID=%s"
			cursor.execute(sql, user_ID)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("delete_record.html",data=data)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session['logged_in']=False
	return redirect(url_for("home"))

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
