from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

codey = Blueprint('codey', __name__)

### Helper Methods

# Executes a SQL select statement
def get_request_db(stmt):
    cursor = db.get_db().cursor()
    cursor.execute(stmt)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    return the_response

# Executes a SQL delete statement
def del_request_db(stmt):
    cursor = db.get_db().cursor()
    cursor.execute(stmt)
    db.get_db().commit()
    the_response = make_response(jsonify(message='Deleted Successfully!'))
    the_response.status_code = 200
    return the_response

# Executes a SQL insert statement
def post_request_db(stmt):
    cursor = db.get_db().cursor()
    cursor.execute(stmt)
    db.get_db().commit()
    the_response = make_response(jsonify(message='Created Successfully!'))
    the_response.status_code = 200
    return the_response

# Executes a SQL update statement
def put_request_db(stmt):
    cursor = db.get_db().cursor()
    cursor.execute(stmt)
    db.get_db().commit()
    the_response = make_response(jsonify(message='Updated Successfully!'))
    the_response.status_code = 200
    return the_response

### User Routes

# Gets all users from the DB
@codey.route('/users', methods=['GET'])
def get_users():
    query = 'select first_name, last_name, user_id from Users'
    return get_request_db(query)

# Creates a new user with the given information.
@codey.route('/users', methods=['POST'])
def add_user():
    req_data = request.get_json()
    first = req_data['first_name']
    last = req_data['last_name']

    query = 'INSERT INTO Users (first_name, last_name) VALUES ("' + \
        first + '", "' + last + '")'

    return post_request_db(query)

# Gets information for the given userID from DB
@codey.route('/users/<user_id>', methods=['GET'])
def get_user_info(user_id):
    query = 'select first_name, last_name, user_id from Users where user_id = %s' % user_id
    return get_request_db(query)

# Deletes the user with the given userID from DB
@codey.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    query = 'delete from Users where user_id = %s' % user_id
    return del_request_db(query)

# Updates the user with the given userID.
@codey.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
    req_data = request.get_json()
    first = req_data['first_name']
    last = req_data['last_name']

    query = 'update Users set first_name = "' + first + \
        '", last_name = "' + last + '" where user_id ="' + user_id + '"'
    
    return put_request_db(query)

### Messages Routes

# Gets all messages from the DB
@codey.route('/messages', methods=['GET'])
def get_messages():
    query = 'select * from Messages'
    return get_request_db(query)

# Creates a new message
@codey.route('/messages', methods=['POST'])
def add_message():
    req_data = request.get_json()
    sender_id = req_data["sender_id"]
    recipient_id = req_data["recipient_id"]
    content = req_data["content"]

    query = 'INSERT INTO Messages (sender_id, recipient_id, content) VALUES ("%s", "%s", "%s")' % (sender_id, recipient_id, content)

    return post_request_db(query)

# Gets the all messages sent to a user
@codey.route('/messages/<recipient_id>', methods=['GET'])
def get_messages_received_by(recipient_id):
    query = 'select sender_id, recipient_id, content, sent_at, message_id from Messages where recipient_id = %s' % recipient_id
    return get_request_db(query)

# Gets the all messages sent between two users
@codey.route('/messages/<user1>/<user2>', methods=['GET'])
def get_messages_between(user1, user2):
    query = 'select sender_id, recipient_id, content, sent_at, message_id, user_id, first_name, last_name '
    query += 'from Messages '
    query += 'join Users on sender_id = user_id '
    query += 'where (sender_id = "' + user1 + \
        '" && recipient_id = "' + user2 + '") '
    query += '|| (sender_id = "' + user2 + \
        '" && recipient_id = "' + user1 + '") '
    query += 'order by sent_at desc;'
    
    return get_request_db(query)

### Shopping Items Routes

# Gets shopping items 
@codey.route('/shoppingItems', methods=['GET'])
def get_shopping_items():
    query = 'select first_name, last_name, item_name, quantity, details, category_id, assigned_to from ShoppingItems Join Users on ShoppingItems.assigned_to = Users.user_id'
    return get_request_db(query)

# Creates a new shopping item
@codey.route('/shoppingItems', methods=['POST'])
def add_shopping_items():
    req_data = request.get_json()

    item_name = req_data['item_name']
    quantity = req_data['quantity']
    details = req_data['details']
    category_id = req_data['category_id']
    assigned_to = req_data['assigned_to']

    query = 'insert into ShoppingItems (item_name, quantity, details, category_id, assigned_to) '
    query += 'values ("%s", "%s", "%s", "%s", "%s")' % (item_name, quantity, details, category_id, assigned_to)
    
    return post_request_db(query)

# Gets the assigned_to for shopping items
@codey.route('/shoppingItems/<assigned_to>', methods=['GET'])
def get_shopping_items_assigned_to_info(assigned_to):
    query = 'select assigned_to, item_id, item_name, quantity, details, category_id from ShoppingItems where assigned_to = %s' % assigned_to
    return get_request_db(query)

### Shopping Categories Routes

# Gets all shopping categories from the DB
@codey.route('/shopping_categories', methods=['GET'])
def get_shopping_categories():
    query = 'select category_name, category_id from ShoppingCategories'
    return get_request_db(query)

# Adds a new shopping category 
@codey.route('/shopping_categories', methods=['POST'])
def add_shopping_category():
    req_data = request.get_json()
    category_name = req_data['category_name']
    query = 'insert into ShoppingCategories (category_name) values ("%s")' % category_name

    return post_request_db(query)

