import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL2']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    cpf = db.Column(db.Integer)

db.create_all()

@app.route('/user', methods=['POST']) 
def inserir_user():
    my_params = request.form
    db.session.add(User(username=my_params.get("username"), email=my_params.get("email"), cpf = my_params.get("cpf")))
    db.session.commit()
    return "Usuário inserido com sucesso", 200

@app.route('/user/<id>') 
def get_user(id):
    user = User.query.filter_by(id=id).first()
    data = {}
    data['username'] = user.username
    data['email'] = user.email
    data['cpf'] = user.cpf
    return json.dumps(data)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return "Usuário deletado com sucesso", 200

@app.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    my_params = request.form
    user = User.query.filter_by(id=id).first()
    user.username = my_params.get("username")
    user.email = my_params.get("email")
    user.cpf = my_params.get("cpf")
    db.session.commit()
    return "Usuário alterado com sucesso", 200

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    T = []
    for user in users:
        data = {}
        data['username'] = user.username
        data['email'] = user.email
        data['cpf'] = user.cpf
        T.append(data)
    return json.dumps(T)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
