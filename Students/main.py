from flask import Flask, render_template, url_for, session, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:viona@localhost/assessment1'
app.config['SECRET_KEY'] = 'vionag'

db = SQLAlchemy(app)


# Creating Student Entity
class Students(db.Model):
    id = db.Column(db.Integer, primary_key='True')
    name = db.Column(db.String(100))
    # foreign key reference
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())
    # classes = db.relationship('Classes', backref='students', lazy=)

    def __init__(self, name):
        self.name = name


# Creating Class Entity
class Classes(db.Model):
    id = db.Column(db.Integer, primary_key='True')
    name = db.Column(db.String(100))
    # class_leader = db.Column(db.Integer, db.ForeignKey('students.id'))
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())
    # relationship with student entity
    students = db.relationship('Students', backref='classes', lazy='joined')

    def __init__(self, name):
        self.name = name


# method to view students table
@app.route('/', methods=['GET', 'POST'])
def show_all():
    db.create_all()
    return render_template('student_table.html', students=Students.query.all())


# method to add a new student
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'])
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('new.html')


# method to pass student details to be updated
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('id')
        student = Students.query.filter_by(id=id).first()
        return render_template('update.html', student=student)


# method to update student record
@app.route('/update_rec', methods=['POST'])
def update_rec():
    if not request.form['name']:
        flash('Please enter all the fields', 'error')
    else:
        id = request.form.get('id')
        student = Students.query.filter_by(id=id).first()
        print(student.name)
        student.name = request.form['name']
        student.updated_on = db.func.now()
        db.session.commit()
    return render_template('student_table.html', students=Students.query.all())


# method to delete a student record
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        student_id = request.form.get('id')
        student = Students.query.filter_by(id=student_id).first()
        db.session.delete(student)
        db.session.commit()
    return render_template('student_table.html', students=Students.query.all())


# method to view class table
@app.route('/classes', methods=['GET', 'POST'])
def classes():
    return render_template('classes.html', classes=Classes.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug='True')





