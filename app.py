from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# mysql配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "jackyWU0225"
DATABASE = "9900_demo"
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

class Forum(db.Model):
    __tablename__ = 'forum'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title  = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship('User', backref='forums')


@app.route('/user/add')
def add_user():
    user = User(username='testuser', password='111111')
    db.session.add(user)
    db.session.commit()
    return 'success'


@app.route('/user/query')
def query_user():
    user = User.query.get(1)  #按照主键查找,一条条查询
    print(f'{user.id}:{user.username}:{user.password}')
    users = User.query.filter_by(username='testuser')  #按照条件查找
    return 'success'

@app.route('/user/update')
def update_user():
    user = User.query.filter_by(username='testuser').first()
    user.password = '1111'
    db.session.commit()
    return 'success'

@app.route('/user/delete')
def delete_user():
    user = User.query.get(1)
    db.session.commit()
    return 'success'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello test'


if __name__ == '__main__':
    app.run()
