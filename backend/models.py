from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    scores = db.relationship("Score", backref="user", cascade="all, delete", lazy=True)
    
    def __init__(self, email, password, full_name, role=role, is_admin=False):
        self.email = email
        self.password_hash = generate_password_hash(password) # generate_password_hash(password)
        self.full_name = full_name
        self.is_admin = is_admin
        self.role = role

    def correct_pass(self,password):
        return check_password_hash(self.password_hash,password)

    def convert_to_json(self):
        return {
            'id': self.id,
            'name': self.full_name,
            'email': self.email
        }
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(120), nullable=False)
    about =db.Column(db.String(120), nullable=False)

    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete", lazy=True)

    def convert_to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about
        }

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(120), nullable=False)
    about =db.Column(db.String(120), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete", lazy=True)

    def convert_to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name,
        }
    
    # def get_subject(self):  
    #     print(self.subject_id,'sdfgh')
    #     return Subject.query.filter_by(id=self.subject_id).first()
    
    # def subject1(self):
    #     return Subject.query.filter(id == self.subject_id).first()
    
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(120), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    duration = db.Column(db.Integer)
    end_date = db.Column(db.Date)
    end_time = db.Column(db.Time)
    start_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    created_at = db.Column(db.DateTime, default=datetime.now)

    
    questions = db.relationship("Question", backref="quiz", cascade="all, delete", lazy=True)
    scores = db.relationship("Score", backref="quiz", cascade="all, delete", lazy=True)
    
    # def get_chapter(self):
    #     return Chapter.query.filter_by(id = self.chapter_id).first()
    
    def start(self):
        return datetime.combine(self.start_date, self.start_time)  
    def end(self):
        return datetime.combine(self.end_date, self.end_time)  

    def convert_to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'end_time': self.end_time.strftime('%H:%M:%S') if self.end_time else None,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'start_time': self.start_time.strftime('%H:%M:%S') if self.start_time else None,
            'chapter_id': self.chapter_id,
            'chapter_name': self.chapter.name,
        }

    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question =db.Column(db.String(500), nullable=False)
    options = db.Column(db.Text, nullable=False) 
    correct = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    # def get_quiz(self):
    #     return Quiz.query.filter_by(id = self.quiz_id).first()
    
    def add_options(self,data):
        print(data)
        if len(data)!= 4:
            # it will raise error when lenth of data which is options of our question 
            # it must be 4
            raise ValueError("There must be exactly 4 options")
        self.options = json.dumps(data) 
    
    def load_options(self):
        return json.loads(self.options)

    def convert_to_json(self):
        return {
            'id': self.id,
            "question": self.question,
            "duration": self.quiz.duration,
            "options": self.load_options(),
            "correct": self.correct,
            "quiz_id": self.quiz_id,
            "quiz_name": self.quiz.name
        }    
    
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id =  db.Column(db.Integer, db.ForeignKey('quiz.id'))
    end_time = db.Column(db.Time)
    percentage =  db.Column(db.Integer)
    answers = db.Column(db.Text, nullable=False) 
    start_time = db.Column(db.Time)
    # def get_quiz(self):
    #     return Quiz.query.filter_by(id = self.quiz_id).first()
    # def get_user(self):
    #     return User.query.filter_by(id = self.user_id).first()
    
    def add_answers(self,data):
        self.answers = json.dumps(data) 
    
    def load_answers(self):
        return json.loads(self.answers)    

    def convert_to_json(self):
        return {
            'id': self.id,
            "end_time": self.end_time.strftime("%H:%M:%S") if self.end_time else None,
            "percentage": self.percentage,
            "answers": self.load_answers(),
            "start_time": self.start_time.strftime("%H:%M:%S") if self.start_time else None,
            "quiz_id": self.quiz.id,
            "quiz_name": self.quiz.name,
            "end_time": self.quiz.end_time.strftime("%H:%M:%S") if self.start_time else None,
            "chapter_name":self.quiz.chapter.name
        }
        