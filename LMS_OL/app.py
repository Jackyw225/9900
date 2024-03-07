from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask app setup
app = Flask(__name__)

# Configuration class for your database settings
class Config:
    DB_USERNAME = 'root'
    DB_PASSWORD = '9900w16a'
    DB_HOST = 'localhost'
    DB_NAME = '9900'
    SECRET_KEY = 'a16w0099'
    # Building the SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Apply the configuration to the Flask app
app.config.from_object(Config)

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# 初始化 Flask-Migrate
migrate = Migrate(app, db)

# Model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    courses = db.relationship('Course', backref='teacher', lazy=True)
    enrolled_courses = db.relationship('Course', secondary='enrollment',
                                       backref=db.backref('enrolled_users', lazy='dynamic'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# Ensure the database tables are created with app context
with app.app_context():
    db.create_all()

# Route for the home/login page
@app.route('/')
def login():
    return render_template('login.html')

# Route to handle login logic
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = user.username
        session['email'] = user.email
        return redirect(url_for('profile'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

# Route for registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Route to handle registration logic
@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('profile'))

# Route for user profile
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('profile.html', username=username, email=user.email)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/mycourse')
def mycourse():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            courses = Course.query.filter_by(teacher_id=user.id).all()
            return render_template('mycourses.html', courses=courses)
    return redirect(url_for('login'))

@app.route('/create_course')
def create_course():
    return render_template('create_course.html')

@app.route('/create_course', methods=['POST'])
def create_course_post():
    # 从表单获取数据
    name = request.form.get('name')
    code = request.form.get('code')
    user_id = User.query.filter_by(username=session.get('username')).first().id
    # 创建新课程对象
    course = Course(name=name, code=code, teacher_id=user_id)
    # 添加到数据库并提交
    db.session.add(course)
    db.session.commit()
    # 重定向到课程列表页面
    return redirect(url_for('mycourse'))


@app.route('/manage_students/<int:course_id>')
def manage_students(course_id):
    # 从数据库中获取课程信息和学生列表，这里只是示例，具体实现依赖于你的模型
    course = Course.query.get_or_404(course_id)
    # 假设你的 Course 模型有一个与学生相关联的属性
    students = course.enrolled_users.all()
    # 渲染管理学生的页面，传递课程和学生信息
    return render_template('manage_students.html', course=course, students=students)

@app.route('/add_student/<int:course_id>', methods=['POST'])
def add_student(course_id):
    student_username = request.form.get('student_username')
    # 根据用户名查找学生
    student = User.query.filter_by(username=student_username).first()
    if student:
        course = Course.query.get_or_404(course_id)
        # 假设存在添加学生到课程的逻辑
        course.enrolled_users.append(student)
        db.session.commit()
    return redirect(url_for('manage_students', course_id=course_id))

@app.route('/delete_student/<int:course_id>/<int:student_id>')
def delete_student(course_id, student_id):
    course = Course.query.get_or_404(course_id)
    student = User.query.get(student_id)
    if student:
        # 假设存在从课程删除学生的逻辑
        course.enrolled_users.remove(student)
        db.session.commit()
    return redirect(url_for('manage_students', course_id=course_id))


# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


def add_test_data():
    # 创建用户
    user1 = User(email='user1@example.com', username='user1', password='password1')
    user2 = User(email='user2@example.com', username='user2', password='password2')
    user3 = User(email='user3@example.com', username='user3', password='password3')
    user4 = User(email='user4@example.com', username='user4', password='password4')

    # 添加用户到数据库
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()

    # 创建课程
    course1 = Course(name='Mathematics 101', code='MATH101', teacher_id=user1.id)
    course2 = Course(name='Physics 101', code='PHYS101', teacher_id=user1.id)

    # 添加课程到数据库
    db.session.add(course1)
    db.session.add(course2)
    db.session.commit()

    # 为课程注册学生
    enrollment1 = Enrollment(user_id=user2.id, course_id=course1.id)
    enrollment2 = Enrollment(user_id=user3.id, course_id=course1.id)
    enrollment3 = Enrollment(user_id=user2.id, course_id=course2.id)
    enrollment4 = Enrollment(user_id=user3.id, course_id=course2.id)

    # 添加选课信息到数据库
    db.session.add(enrollment1)
    db.session.add(enrollment2)
    db.session.add(enrollment3)
    db.session.add(enrollment4)
    db.session.commit()

    print("Test data added successfully!")

# 确保这个函数只在你想要添加测试数据的时候调用
if __name__ == '__main__':
    with app.app_context():
        # 首先尝试删除所有数据（慎用，只在测试环境中使用）
        db.drop_all()
        # 创建数据库表
        db.create_all()
        # 添加测试数据
        add_test_data()
    app.run(debug=True)
