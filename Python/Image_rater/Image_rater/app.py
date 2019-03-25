from flask import Flask, request, render_template
app = Flask(__name__)

class Image():

	def __init__(self, filename, credit):
		self.filename = filename
		self.credit = credit
		self.ratings = []
		self.average = 0

	def add_rating(self, input):
		self.ratings.append(input)

	def find_average(self):
		result = 0
		for rating in ratings:
			result += rating
		result = result / len(self.ratings)
		self.average = result


images = []
import os
path = os.getcwd()+"/static/images"
for filename in os.listdir(path):
	images.append(Image(filename, "Savage Chickens, Doug Savage"))
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods = ["GET", "POST"])
def index():
    
    return render_template('index.html', images = images)

@app.route('/rate', methods = ["GET", "POST"])
def rate():
    '''
    for image in images():
        if image == request.args("imageName"):
            is_image = True
            picture = image
        else:
            is_image = False
    if request.method == "POST":
        form = request.form
        value = int(form["rate"])
        picture.add_rating(value)
        picture.find_average()
        return render_template('rate.html', rating = "This image has been rated: " + picture.average + " Stars.")
    '''
    return render_template('rate.html', rating = "No Rating Added")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug = True)
