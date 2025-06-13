from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from bson.json_util import dumps
from app import mongo

users_bp = Blueprint('users_bp', __name__)
api_bp = Blueprint('api_bp', __name__, url_prefix='/api/users')


# ----------------------- JINJA FRONTEND ROUTES -----------------------

@users_bp.route('/')
def index():
    users = mongo.db.people.find()
    return render_template('index.html', users=users)

@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        mongo.db.people.insert_one({'name': name, 'email': email, 'password': password})
        return redirect(url_for('users_bp.index'))
    return render_template('add_user.html')

@users_bp.route('/update/<id>', methods=['GET', 'POST'])
def update_user(id):
    user = mongo.db.people.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        update_data = {'name': name, 'email': email}
        if password:
            update_data['password'] = generate_password_hash(password)
        mongo.db.people.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        return redirect(url_for('users_bp.index'))
    return render_template('update_user.html', user=user)

@users_bp.route('/delete/<id>')
def delete_user(id):
    mongo.db.people.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('users_bp.index'))


# ------------------------- RESTFUL API ROUTES ------------------------

@api_bp.route('/', methods=['GET'])
def get_users():
    users = mongo.db.people.find()
    return dumps(users), 200

@api_bp.route('/<id>', methods=['GET'])
def get_user(id):
    try:
        user = mongo.db.people.find_one({'_id': ObjectId(id)}, {'password': 0})
        if user:
            return dumps(user), 200
        return jsonify({'error': 'User not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400

@api_bp.route('/', methods=['POST'])
def create_user_api():
    data = request.json
    if not all(k in data for k in ("name", "email", "password")):
        return jsonify({'error': 'Missing fields'}), 400
    hashed_pw = generate_password_hash(data['password'])
    user_id = mongo.db.people.insert_one({
        'name': data['name'],
        'email': data['email'],
        'password': hashed_pw
    }).inserted_id
    return jsonify({'message': 'User created', 'id': str(user_id)}), 201

@api_bp.route('/<id>', methods=['PUT'])
def update_user_api(id):
    data = request.json
    updates = {}
    if 'name' in data:
        updates['name'] = data['name']
    if 'email' in data:
        updates['email'] = data['email']
    if 'password' in data:
        updates['password'] = generate_password_hash(data['password'])

    if not updates:
        return jsonify({'error': 'No fields to update'}), 400

    try:
        result = mongo.db.people.update_one({'_id': ObjectId(id)}, {'$set': updates})
        if result.matched_count:
            return jsonify({'message': 'User updated'}), 200
        return jsonify({'error': 'User not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400

@api_bp.route('/<id>', methods=['DELETE'])
def delete_user_api(id):
    try:
        result = mongo.db.people.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'User deleted'}), 200
        return jsonify({'error': 'User not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400
