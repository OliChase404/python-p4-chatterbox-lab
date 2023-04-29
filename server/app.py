from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/', methods=['GET'])
def root():
    return '<h1>Welcome to Chatterbox!</h1>'


@app.route('/messages', methods=['POST', 'GET'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        messages_dicts = [message.to_dict() for message in messages]
        response = make_response(jsonify(messages_dicts), 200)
    
    elif request.method == 'POST':
        # data = request.get_json()
        message = Message()
        for key in request.json:
            setattr(message, key, request.json[key])
        
        db.session.add(message)
        db.session.commit()
        response = make_response(jsonify(message.to_dict()), 201)
        
    return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    
    
    if request.method == 'GET':    
        response = make_response(jsonify(message.to_dict()), 200)
    
    elif request.method == 'PATCH':
        message = Message.query.get(id)
        for attr in request.json:
            setattr(message, attr, request.json[attr])
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)
    
    elif request.method == 'DELETE':
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        response = make_response(jsonify(message.to_dict()), 204)
    
    return response
    

if __name__ == '__main__':
    app.run(port=5555)
