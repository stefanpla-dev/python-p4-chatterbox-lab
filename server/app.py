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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        dicts = []
        for message in messages:
            dicts.append(message.to_dict())
        return dicts, 200
        # return [message.to_dict() for message in messages], 200
    elif request.method =='POST':
        json_data = request.get_json()
        new_message = Message(
            body=json_data.get('body'),
            username=json_data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id==id).first()

    if message is None:
        return {'error': 'Message not found'}, 404

    if request.method == 'GET':
        return message.to_dict(), 200

    elif request.method == 'PATCH':
        json_data = request.get_json()
        if 'body' in json_data:
            message.body = json_data.get('body')

        db.session.add(message)
        db.session.commit()

        return message.to_dict(), 202
        
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return {}, 204

if __name__ == '__main__':
    app.run(port=5555)
