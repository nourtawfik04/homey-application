from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

emma = Blueprint('emma', __name__)

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

### Tasks Routes

# Gets information for all tasks from DB
@emma.route('/tasks', methods=['GET'])
def get_tasks_info():
    query = 'select first_name, last_name, assigned_to, category_id, complete_by, title, details, '
    query += 'task_status, task_id, created_by from Tasks Join Users on Tasks.assigned_to = Users.user_id '
    query += 'order by complete_by asc'
    return get_request_db(query)

# Creates a new task
@emma.route('/tasks', methods=['POST'])
def add_task():
    req_data = request.get_json()

    assigned_to = req_data['assigned_to']
    title = req_data['title']
    details = req_data['details']
    task_status = req_data['task_status']
    complete_by = req_data['complete_by']
    created_by = req_data['created_by']
    category_id = req_data['category_id']

    query = 'insert into Tasks (assigned_to, title, details, task_status, complete_by, created_by, category_id) '
    query += 'values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (assigned_to, title, details, task_status, complete_by, created_by, category_id)
    
    return post_request_db(query)

# Gets tasks in the given category
@emma.route('/tasks/<category_id>', methods=['GET'])
def get_tasks_in_category(category_id):
    query = 'select category_id, task_id from Tasks where category_id= %s' % category_id
    return get_request_db(query)


# Gets all tasks assigned to the given user
@emma.route('/tasks/<assigned_to>', methods=['GET'])
def get_task_assignee_info(task_id):
    query = 'select assigned_to, task_id from Tasks where task_id = %s' % task_id
    return get_request_db(query)

# Updates a task 
@emma.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    req_data = request.get_json()
    assigned_to = req_data['assigned_to']
    title = req_data['title']
    details = req_data['details']
    task_status = req_data['task_status']
    complete_by = req_data['complete_by']
    created_by = req_data['created_by']
    category_id = req_data['category_id']
    query = 'update Tasks set assigned_to = "%s", title = "%s", details = "%s", task_status ="%s", complete_by = "%s", created_by =  "%s", category_id = "%s" where task_id = "%s"' % (assigned_to, title, details, task_status, complete_by, created_by, category_id, task_id)
    return put_request_db(query)

# Deletes the given task
@emma.route('/tasks/<task_id>', methods=['DELETE'])
def del_tasks_info(task_id):
    query = 'delete from Tasks where task_id = %s' % task_id
    return del_request_db(query)

### Task Categories Routes

# Gets all task categories from the DB
@emma.route('/task_categories', methods=['GET'])
def get_task_categories():
    query = 'select category_name, category_id from TaskCategories'
    return get_request_db(query)

# Adds a new task category
@emma.route('/task_categories', methods=['POST'])
def add_task_category():
    req_data = request.get_json()
    category_name = req_data['category_name']
    query = 'insert into TaskCategories (category_name) values ("%s")' % category_name

    return post_request_db(query)

### Events Routes

# Gets all events from the DB
@emma.route('/events', methods=['GET'])
def get_events():
    query = 'select title, details, scheduled, created_by, event_id from Events order by scheduled asc'
    return get_request_db(query)

# Adds a new event to the DB
@emma.route('/events', methods=['POST'])
def add_event():
    req_data = request.get_json()
    title = req_data['title']
    details = req_data['details']
    scheduled = req_data['scheduled']
    created_by = req_data['created_by']

    query = 'insert into Events (title, details, scheduled, created_by) values ' + \
       '("%s", "%s", "%s", "%s")' % (title, details, scheduled, created_by)

    return post_request_db(query)

# Gets info for a given event from the DB
@emma.route('/events/<event_id>', methods=['GET'])
def get_events_info(event_id):
    query = 'select title, details, scheduled, created_by, event_id from Events where event_id = %s' % event_id

    return get_request_db(query)

# Update the given event in the DB
@emma.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    req_data = request.get_json()
    title = req_data['title']
    details = req_data['details']
    scheduled = req_data['scheduled']
    query = 'update Events set title = "%s", details = "%s", scheduled = "%s" where event_id = "%s"' % (title, details, scheduled, event_id)
    
    return put_request_db(query)

# Delete the event from the DB
@emma.route('/events/<event_id>', methods=['DELETE'])
def del_events_info(event_id):
    query = 'delete from Events where event_id = %s' % event_id
    
    return del_request_db(query)
