from flask import Flask, render_template, request, redirect, url_for
import pymysql
#from flaskext.mysql import MySQL
app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
# Connect to the database
def create_connection():
    return pymysql.connect(host='localhost',
                             user='root',
                             password='13COM',
                             db='sampythondb',
                             charset='utf8mb4'
                             ,cursorclass=pymysql.cursors.DictCursor)

#display users
@app.route('/')
def hello():
    connection=create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from users"
            cursor.execute(sql)
            data = cursor.fetchall()
            data=list(data)
    finally:
            connection.close()


    return render_template("index.html", results=data)

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
         dob="2001-10-01"
         try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (FirstName,FamilyName,Email,DateOfBirth,Password) VALUES (%s,%s,%s,%s,%s)"
                val=(first_name,family_name,email,dob,password)
                cursor.execute(sql,(val))
                #save values in dbase
            connection.commit()
            cursor.close()
            with connection.cursor() as cursor:
                #pull records and display
                sql = "SELECT * from users"
                cursor.execute(sql)
                data = cursor.fetchall()
                data=list(data)
         finally:
             connection.close()
         return redirect(url_for('hello'))
   return render_template("add_user.html")



@app.route('/edit_record', methods=['POST','GET'])
def update_user():
	user_id = request.args.get('id')
	connection=create_connection()
	if request.method == 'POST':
			form_values = request.form 
			first_name = form_values.get("firstname")
			family_name = form_values.get("familyname")
			email = form_values.get("email")
			password = form_values.get("password")
			dob="2001-10-01"
			user_id = form_values.get('ID')

			try:
				with connection.cursor() as cursor:
					# Create a new record
					sql = "UPDATE `users` SET FirstName=%s,FamilyName=%s,Email=%s,DateOfBirth=%s,Password=%s WHERE ID=%s"
					val=(first_name,family_name,email,dob,password, user_id)
					cursor.execute(sql,(val))
					data = cursor.fetchall()
					data=list(data)
					#save values in dbase
				connection.commit()
				cursor.close()
			finally:
				connection.close()
			return redirect(url_for('hello'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_id)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("Edit_record.html",data=data)
# Tasks 
# Per assessment AS91902 Document; complex techniques  include creating queries which insert, update or delete to modify data
#so you should add  new routes for edit_user, user_details and delete_user using record ids
# create the html pages needed
# modify database to include an image field which will store the image filename(eg pic.jpg) in database and  implement this functionality in code where applicable

@app.route('/delete_record', methods =["GET","POST"])
def delete_record():
	user_ID = request.args.get("id")
	connection=create_connection()
	if request.method == "POST":
		form = request.form
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "DELETE FROM  `users` WHERE ID = %s "
				val=(user_ID)
				cursor.execute(sql,(val))
				data = cursor.fetchall()
				data=list(data)
			#save values in dbase
			connection.commit()
			cursor.close()
		finally:
			connection.close()
			return redirect(url_for('hello'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_ID)
			data = cursor.fetchone()
			data=data
	finally:
		connection.close()
	return render_template("delete_record.html",data=data)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
