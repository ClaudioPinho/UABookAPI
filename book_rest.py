from flask import Flask
from flask_restful import Resource, Api, reqparse
import psycopg2
import json
import collections

#Store the app name
appName = "UA BOOKS"

#Connect to the database
conn = psycopg2.connect(database="UABooks", user="postgres", password="uaadmin123", host="localhost", port="5432")
cursor = conn.cursor()

app = Flask(appName)
api = Api(app)

class Book:
	def __init__(self, biblio_number, framework_code, author, title, uni_title, notes, serial, series_title, copyright_date, timestamp, date_created, abstract):
		self.book = {
			'biblio_number': biblio_number,
			'framework_code': framework_code,
			'author': author,
			'title': title,
			'uni_title': uni_title,
			'notes': notes,
			'serial': serial,
			'series_title': series_title,
			'copyright_date': copyright_date,
			'timestamp': timestamp,
			'date_created': date_created,
			'abstract': abstract
			}

	def toJson(self):
		return self.book

class BookRequester(Resource):
	def get(self):
		#Define the parameters to receive
		parser = reqparse.RequestParser()
		parser.add_argument('title', required=True, type=str)
		#parser.add_argument('author')
		args = parser.parse_args()

		#Convert the arguments to variables
		book_title = args['title'] #Needed
		#book_author = args['author'] #Optional
		#
		cursor.execute("SELECT * FROM \"Book\" WHERE title like (%s);", (book_title,))
		fetch = cursor.fetchall()
		results = []
		for x in range(0, len(fetch)):
			biblionumber = fetch[x][0]
			frameworkcode = fetch[x][1]
			author = fetch[x][2]
			title = fetch[x][3]
			unititle = fetch[x][4]
			notes = fetch[x][5]
			serial = fetch[x][6]
			seriestitle = fetch[x][7]
			copyrightdate = fetch[x][8]
			timestamp = fetch[x][9].strftime("%d-%m-%Y (%H:%M:%S)")
			datecreated = fetch[x][10].strftime("%d-%m-%Y (%H:%M:%S)")
			abstract = fetch[x][11]
			results.append(Book(biblionumber,frameworkcode,author,title,unititle,notes,serial,seriestitle,copyrightdate,timestamp,datecreated,abstract).toJson())
		return results

#Adds a resource to the API
api.add_resource(BookRequester, '/book')
#Runs the API
app.run(host='0.0.0.0', debug=True)
