# Import Dependencies
from flask import Flask, render_template, request
from os import path
import json

app = Flask(__name__)

# Part 1 

# Get courses from JSON
# Courses is a list of dictionaries. 
# Uncomment to view the print out on your command line tool. 
with open('student_courses.json') as d:
  course_data = json.load(d)

courses = course_data['courses']
students = course_data['students']
numCourses = len(courses)

coursesWithStudents = [[] for i in range(numCourses)]

for student in students:
	for courseID in student['courses']:
		coursesWithStudents[courseID - 1].append(student['name'])


with open('output.txt', 'w') as f:
	for i in range(numCourses):
		f.write(courses[i]['name'] + ':')
		for student in coursesWithStudents[i]:
			f.write(' ' + student + ',')
		f.write('\n')

# Part 2

images = [
  'https://mediaproxy.salon.com/width/1200/height/675/https://media.salon.com/2020/09/calculus-algebra-0925201.jpg',
	'https://www.insidescience.org/sites/default/files/2020-06/physics-chalkboard_cropped.jpg',
	'https://www.freecodecamp.org/news/content/images/2021/08/chris-ried-ieic5Tq8YMk-unsplash.jpg',
	'http://studybreaks.com/wp-content/uploads/2016/08/635909393667865802-60346571_stack_of_books.jpg',
	'https://images.newscientist.com/wp-content/uploads/2021/02/23162716/chemistry.jpg',
	'https://miro.medium.com/max/640/1*Fne1ZRCpE7Y4uCp0bnk0Hg.jpeg',
	'https://i.cbc.ca/1.6338108.1643915795!/fileImage/httpImage/philosophers.jpg',
	'https://www.cato.org/sites/cato.org/files/styles/optimized/public/2021-01/GettyImages-1127256104%20%281%29.jpg?itok=fJ2uAJCi',
	'https://i.pinimg.com/736x/3a/7f/b1/3a7fb18b341503d41034e6d79bcd328d.jpg',
	'https://images.unsplash.com/photo-1521295121783-8a321d551ad2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Z2VvZ3JhcGh5fGVufDB8fDB8fA%3D%3D&w=1000&q=80'
          ]

 
# Check if file exists
if path.isfile('reviews.json') is False:
  raise Exception("File not found")

reviewsFile = open('reviews.json')
reviews = json.load(reviewsFile)


# Render using "courses.html"
# Note: "courses.html" can be found in the "templates" folder
# CSS file in static/css adds formating to the template as well
# Provide courses as an argument to the html
@app.route('/')
def home_page():
	return render_template('home_page.html', arg = courses, coursesWithStudents = coursesWithStudents, images = images)


@app.route('/course/<courseID>', methods = ['GET', 'POST'])
def course_page(courseID):
	courseID = int(courseID)
	if (request.method == 'GET'):
		courseReviews = reversed([review for review in reviews if review['courseID'] == courseID])
		return render_template('course_page.html', course = courses[courseID - 1], image = images[courseID - 1], coursesWithStudents = coursesWithStudents, reviews = courseReviews)	

	if (request.method == 'POST'):
		data = request.form
		newReview = {
			'courseID': courseID,
			'name': data['name'],
			'data': data['review']
		}
		reviews.append(newReview)
		with open('reviews.json', 'w') as rf:
			json.dump(reviews, rf, indent = 2)
		courseReviews = reversed([review for review in reviews if review['courseID'] == courseID])
		return render_template('course_page.html', course = courses[courseID - 1], image = images[courseID - 1], coursesWithStudents = coursesWithStudents, reviews = courseReviews)	


if __name__ == '__main__':
	app.debug = True
	app.run(host = 'localhost', port = 5000)