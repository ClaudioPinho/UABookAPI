import psycopg2
import random
try:
	connection = psycopg2.connect(user = "postgres",
								password = "admin",
								host = "127.0.0.1",
								port = "5432",
								database = "UABooks")
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM public.\"Book\"")
	record = cursor.fetchall()
		
	for i in range(0, len(record)):
		bookID = record[i][0]
		rndShelf = random.randint(1, 14)
		rndShelfNumber = random.randint(1, 8)
		#print(book)
		command = "INSERT INTO \"BookPosition\" (\"biblionumber\", \"shelfnumber\", \"shelfposition\") values ({}, {}, {})".format(bookID, rndShelf, rndShelfNumber)
		cursor.execute(command)
	connection.commit()
	#for row in record:
	#	cursor.execute("INSERT INTO \"BookPosition\" (\"biblionumber\", \"shelfnumber\", \"shelfposition\") values ({}, {}, {})".format());

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
finally:
	#closing database connection.
	if(connection):
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")