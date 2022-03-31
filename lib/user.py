from flask import session
from lib.db import connect
import bcrypt

# Returns back a user
def get_user(key: str, value: str):
	cursor = connect().cursor()
	query = ("SELECT user_id, username, password FROM Users "
	         "WHERE " + key + "=%s")

	cursor.execute(query, (value, ))
	for (user_id, username, password) in cursor:
		return {
			"user_id": user_id,
			"username": username,
			"password": password,
		}

# Retrieves back the user_id for login credentials, only if
# the password is correct
def get_user_id_check_password(username: str, password_hash: str):
	user = get_user('username', username)
	if user is None:
		return None

	password = user['password'].encode('utf8')
	password_hash = password_hash.encode('utf8')

	if bcrypt.checkpw(password_hash, password):
		return user['user_id']

	return None

# Takes username and password from the request and tries to log in
# Type = user type (hospital, place, ...)
def try_login(request, user_type: str):
	username = request.form.get('username')
	password = request.form.get('password')
	user_id = get_user_id_check_password(username, password)
	if user_id is None:
	    return {
	        'ok': False,
	        'message': 'That user does not exist'  
	    }

	session['user_id'] = user_id
	session['user_type'] = user_type

	return {
		'ok': True
	}

def create_user(username: str, password: str):
	# usernames most of the time should be case insensitive, and definitely
	# not contain spaces
	username = username.lower().strip()
	password = password.strip()

	# Makes sure that username is not taken
	if get_user('username', username) != None:
		return {
			'ok': False,
			'message': 'That username is already taken!'
		}

	if len(password) < 6:
		return {
			'ok': False,
			'message': 'Password must be at least 6 characters long'
		}

	password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

	cursor = connect().cursor()
	query = ("INSERT INTO Users "
               "(username, password) "
               "VALUES (%s, %s)")

	cursor.execute(query, (username, password))
	connect().commit()
	user_id = cursor.lastrowid

	return {
		'ok': True,
		'user_id': user_id,
	}
#get all user
def get_all_user():
    cursor = connect().cursor()
    query = ("SELECT * FROM Users")

    cursor.execute(query, (value, ))
    for (user_id, username, password) in cursor:
        return {
            "user_id": user_id,
            "username": username,
            "password": password,
        }
