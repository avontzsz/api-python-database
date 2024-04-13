from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt()

# Modelo para Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Modelo para Tarefa
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

# Decorador para autenticação com token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Rota para registro de usuário
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário registrado com sucesso!'})

# Rota para login de usuário
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Não foi possível verificar!'}), 401
    
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado!'}), 401
    
    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    
    return jsonify({'message': 'Credenciais inválidas!'}), 401

# Rota para criação de uma nova tarefa
@app.route('/tarefa', methods=['POST'])
@token_required
def criar_tarefa(current_user):
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tarefa criada com sucesso!'})

# Rota para obter todas as tarefas
@app.route('/tarefas', methods=['GET'])
@token_required
def obter_tarefas(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}
        output.append(task_data)
    return jsonify({'tarefas': output})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
