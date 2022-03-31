# Connects to the database. Only makes one connection (Singleton pattern)
import os
import mysql.connector

connection = None

def connect():
	global connection

	if connection is None:
		connection = mysql.connector.connect(
			user=os.getenv('DB_USER'),
			password=os.getenv('DB_PASSWORD'),
			host=os.getenv('DB_HOST'),
			database=os.getenv('DB_NAME')
		)

	return connection