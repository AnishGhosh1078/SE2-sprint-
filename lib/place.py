from lib.db import connect
from lib.user import get_user, create_user

from flask import render_template

# Gets the place record based on some key (username or place_id)
# Used by the get and get_by_username
# This is private function
def _get_place(key: str, value: str):
	cursor = connect().cursor()
	query = ("SELECT user_id, place_id, place_name, address FROM Places "
	         "WHERE " + key + "=%s")

	cursor.execute(query, (value, ))
	for (user_id, place_id, place_name, address) in cursor:
		return {
			"user_id": user_id,
			"place_id": place_id,
			"place_name": place_name,
			"address": address,
		}

	# If the loop is not iterated and this line is reached, place was not found
	return None

# Retrieves a place
def get_place(place_id: str):
	return _get_place('place_id', place_id)

# Retrieves a place record based on the username
def get_place_by_username(username: str):
	return _get_place('username', username)

# Creates (registers) a new place
def create_place(place: dict):
	required_fields = ['name', 'address', 'username', 'password']

	# Check that all fields are present
	for field in required_fields:
		if type(place[field]) is not str or len(place[field]) == 0:
			return {
				'ok': False,
				'message': field + ' is required!'
			}

	create_response = create_user(place.get('username'), place.get('password'))
	if create_response['ok'] is not True:
		return create_response

	query = ("INSERT INTO Places "
               "(user_id, place_name, address) "
               "VALUES (%s, %s, %s)")

	cursor = connect().cursor()
	cursor.execute(query, (
		create_response['user_id'],
		place['name'],
		place['address'],
	))
	connect().commit()
	place_id = cursor.lastrowid

	return {
		'ok': True,
		'place_id': place_id
	}

# Checks a user into a place
def check_in(place_id: str, user: dict):
	required_data = ['name', 'address', 'city']

def render_place_check_in_page(place):
	return render_template('check-in.html', place_name=place['place_name'])

#get_all_places
def get_all_place():
    cursor = connect().cursor()
    query = ("SELECT * FROM Places ")

    cursor.execute(query, (value, ))
    for (user_id, place_id, place_name, address) in cursor:
        return {
            "user_id": user_id,
            "place_id": place_id,
            "place_name": place_name,
            "address": address,
        }

