from flask import Flask, request,send_file
import os
from datetime import timedelta, datetime
from models import db, User, Quiz, Chapter, Question, Subject, Score
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity,create_access_token
from flask_restful import Api, Resource
from flask_caching import Cache
import logging,json,time
from celery import Celery
from celery.schedules import crontab
from cache import cache
from time_utils import time_converter,date_converter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
import csv



from worker import  make_celery 

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'app.sqlite3')
app.config['SECRET_KEY'] = 'quiz-app'
app.config['JWT_SECRET_KEY'] = 'quiz-app-jwt'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)


celery=make_celery(app)


# Now that app/celery/DB are ready, import resources and tasks
from chapter_api import ChapterApi
from quiz_api import QuizApi
from question_api import QuestionApi
from admin_api import AdminApi
from user_api import UserDashboardApi, ExamApi, ResultApi
from plots import UserChartApi, AdminBarChartApi, AdminPieChartApi

class UserApi(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'admin':
            return {'message': 'Access Denied'}, 401
        
        search_query = request.args.get('search', '')

        if search_query:
            users = User.query.filter(User.full_name.ilike(f"%{search_query}%")).all()
        else:
            users = User.query.filter_by(role='user').all() 

        print(users)

        user_list = []

        for user in users:
            user_list.append(user.convert_to_json())
        return user_list, 200

    @jwt_required()
    def delete(self, user_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'admin':
            return {'message': 'Access Denied'}, 401

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found.'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully.'}, 200

class LoginApi(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data.get('email')).first()
        # print(user.email)
        if user:
            if user.correct_pass(data.get('password')):
                identity = {"user_id":user.id, "user_role":user.role}
                token = create_access_token(identity=json.dumps(identity))
                return {
                        'message': 'User logged in successfully.',
                        'token':token,
                        'user_name':user.full_name,
                        'user_role':user.role  
                        }, 200
            return {'message': 'Incorrect Password.'}, 400
        return {'message': "User does not exist."}, 404

class SignupApi(Resource):
    def post(self):
        data = request.json
        if not (data.get('name') and data.get('email') and data.get('password') and  data.get('role')):
            return {'message': ' Bad request! All the data fields are required.'}, 400 

        if len(data.get('name').strip()) > 60 or len(data.get('name').strip()) < 4:
            return {'message': 'Length of name should be in between 4 and 60'}, 400 

        if len(data.get('email').strip()) > 60 or "@" not in data.get('email'):
            return {'message': 'Length of email should be 120 and should contain @'}, 400 

        if len(data.get('password').strip()) > 20 or len(data.get('password').strip()) < 4:
            return {'message': 'Length of password should be in between 4 and 20'}, 400 

        if data.get('role').strip() != 'user':
            return {'message': 'Role should be user.'}, 400 


        user = User.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message': "User already exists."}, 400
        new_user = User(
                        full_name=data.get('name'), 
                        email=data.get('email'),
                        password=data.get('password'),
                        role=data.get('role')
                        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User Signed up successfully'}, 201
        
class WecomeAPI(Resource):
    @jwt_required()
    def get(self):
        print(request)
        print(json.loads(get_jwt_identity().get('user_role')))
        print(json.loads(get_jwt_identity().get('user_id')))
        return {'message': 'Hello, This is Quiz App!'}, 200
    def post(self):

        msg= f'Hello! {request.get_json().get("name")}'
        return {'message': msg}, 200


class SubjectApi(Resource):
    @jwt_required()
    def get(self, subject_id=None):
        if subject_id:  
            subject = Subject.query.get(subject_id)
            if subject:
                return subject.convert_to_json(), 200
            return {'message': 'Subject does not exist.'}, 404
        
        search_query = request.args.get('search', '').strip()
        
        if search_query:
            subjects = Subject.query.filter(Subject.name.ilike(f"%{search_query}%")).all()
        else:
            subjects = Subject.query.all()
        
        sub_list = [sub.convert_to_json() for sub in subjects]
        return sub_list, 200


    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('name') and data.get('about')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 

            if len(data.get('name').strip()) > 120 or len(data.get('name').strip()) < 3:
                return {'message': 'Length of name should be in between 3 and 60'}, 400

            if len(data.get('about').strip()) > 120 or len(data.get('about').strip()) < 3:
                return {'message': 'Length of about section should be in between 3 - 120'}, 400

            subject = Subject.query.filter_by(name=data.get('name').strip()).first()
            if subject:
                return {"message": "Subject already exists."}, 409

            new_subject = Subject(
                            name=data.get('name'), 
                            about=data.get('about')
                            )
            db.session.add(new_subject)
            db.session.commit()
            return {'message': 'Subject added successfully.'}, 201
        return {'message': 'Access Denied'}, 403



    @jwt_required()
    def put(self, subject_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('name') and data.get('about')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 
            

        
            subject = Subject.query.get(subject_id)
            if subject:
                subject.name = data.get('name').strip() if data.get('name') else subject.name
                subject.about = data.get('about').strip() if data.get('about') else subject.about
                db.session.commit()
                return {'message': 'Subject updated successfully.'}, 200 
            return {'message': 'Subject does not exists.'}, 404 
        return {'message': 'Access Denied'}, 403

    @jwt_required()
    def delete(self, subject_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':

            subject = Subject.query.get(subject_id)
            if subject:
                db.session.delete(subject)
                db.session.commit()
                return {'message': 'Subject Deleted successfully.'}, 200 
            return {'message': 'Subject does not exists.'}, 404
        return {'message': 'Access Denied'}, 403


      

class ExportDataApi(Resource):
    @jwt_required()
    def get(self):
        from main import export_users_csv
        logging.info("Exporting data...")
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'admin':
            return {'message': 'Access Denied'}, 401

        users = User.query.filter_by(is_admin=0).all()
        quiz_data = []

        for user in users:
            total_quizzes = Score.query.filter_by(user_id=user.id).count()
            avg_score = db.session.query(db.func.avg(Score.percentage)).filter_by(user_id=user.id).scalar()
            avg_score = round(avg_score, 2) if avg_score else 0  

            quiz_data.append({
                "Name": user.full_name,
                "Email": user.email,
                "total_quizzes": total_quizzes,
                "average_score": avg_score
            })

        task = export_users_csv.delay(quiz_data)
        timeout = 30
        waited = 0

        while not task.ready():

            time.sleep(1)
            waited += 1

            if waited >= timeout:
                return {"message": "Export timed out"}, 500
            if task.failed():
                return {"message": "Export failed"}, 500
        file_path = task.result 
        if not isinstance(file_path, (str, bytes, os.PathLike)) or not os.path.exists(file_path):
            return {'message': 'Invalid file path returned'}, 500

    
        return send_file(file_path, as_attachment=True, download_name="data_exportcsv", mimetype='text/csv')


def add_admin():
    with app.app_context():
        db.create_all()
    admin_user = User.query.filter_by(email='prajwal@gmail.com').first()
    if not admin_user:
        admin = User(
            email='prajwal@gmail.com',
            password='1234',
            is_admin=True,
            full_name='Prajwal',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

# API resource registration
api.add_resource(LoginApi, '/api/login')
api.add_resource(UserApi, '/api/users', '/api/users/<int:user_id>')
api.add_resource(SignupApi, '/api/signup')
api.add_resource(WecomeAPI, '/api/welcome')
api.add_resource(SubjectApi, '/api/subject', '/api/subject/<int:subject_id>')
api.add_resource(ChapterApi, '/api/chapter', '/api/chapter/<int:chapter_id>')
api.add_resource(QuizApi, '/api/quiz', '/api/quiz/')
api.add_resource(QuestionApi, '/api/question', '/api/question/<int:question_id>')
api.add_resource(AdminApi, '/api/admin')
api.add_resource(UserDashboardApi, '/api/user_dash')
api.add_resource(ExamApi, '/api/exam/<int:id>')
api.add_resource(ResultApi, '/api/result/<int:score_id>')
api.add_resource(ExportDataApi, '/api/export/data')
api.add_resource(UserChartApi, "/api/user_chart/image")
api.add_resource(AdminBarChartApi, "/api/admin_bar_chart/image")
api.add_resource(AdminPieChartApi, "/api/admin_pie_chart/image")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    sender.add_periodic_task(10.0, daily_reminder.s(), name='daily report every 10 sec',)
    sender.add_periodic_task(10.0, monthly_report.s(), name='monthly report at every 10 sec ',)

    
    
    # hour=19, minute=30
    sender.add_periodic_task(
        crontab(hour=19, minute=30),
        daily_reminder.s(),
        name='daily_reminder when new quizz is added mail at 07:30 pm',
    )

    sender.add_periodic_task(
        crontab(day_of_month="1", month_of_year="*"),
        monthly_report.s(),
        name='monthly report ',
    )

@celery.task
def test(arg):
    print(arg)

@celery.task
def add(x, y):
    z = x + y
    print(z)

def send_mail(email, subject, email_content, attachment=None):
    # Define email server and credentials
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "prajwal@gmail.com"
    sender_password = ""

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content, "html"))

    if attachment:
        
        with open(attachment, "rb") as attachment_data:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_data.read())
            encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" %os.path.basename(attachment))

        msg.attach(part)


    server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail sent Successfully")

@celery.task
def daily_reminder():

    users = User.query.filter_by(is_admin=False).all()

    today_730_pm = datetime.now().replace(hour=19, minute=30, second=0, microsecond=0)
    yesterday_730_pm = today_730_pm - timedelta(days=1)
    # print(yesterday_730_pm)
    new_quizzes = Quiz.query.filter(
                                    Quiz.created_at >= yesterday_730_pm,
                                    Quiz.created_at < today_730_pm
                                    ).all()

    if len(new_quizzes) > 0:
        for user in users:
            msg = f'<h1>Hello, { user.full_name }! New Quiz has been added, please visit the website. </h1>'
            send_mail(email = user.email, email_content = msg, subject = "Daily Reminder")
    print("Daily Reminder sent!")
    



def get_html_report(username, data):
    with open("app/report.html", "r") as file:
        jinja_template = Template(file.read())
        html_report = jinja_template.render(username=username, data=data)

    return html_report

def generate_monthly_report(user):
    # last month
    last_month = datetime.now().replace(day=1) - timedelta(days=1)
    today = datetime.now()
    first_day_current_month = today.replace(day=1)     
    last_month_end = first_day_current_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)


    scores = Score.query.filter(
        Score.user_id == user.id,
        Quiz.created_at >= last_month_start,
        Quiz.created_at <= last_month_end
    ).all()

    total_quizzes = len(scores)
    average_score = sum([s.percentage for s in scores]) / total_quizzes if total_quizzes > 0 else 0

    # Fetch ranking logic (example: ranking based on percentage)
    rankings = Score.query.order_by(Score.percentage.desc()).all()
    user_rank = next((index + 1 for index, s in enumerate(rankings) if s.user_id == user.id), None)

    report_data = {
        "name": user.full_name,
        "email": user.email,
        "total_quizzes": total_quizzes,
        "average_score": round(average_score, 2),
        "ranking": user_rank if user_rank else "N/A",
        "scores": scores,
        "month": last_month.strftime("%B %Y")
    }

    return report_data




@celery.task
def monthly_report():
    users = User.query.filter_by(is_admin=False).all()
    
    last_month = datetime.now().replace(day=1) - timedelta(days=1)
    

    for user in users:
        report_data = generate_monthly_report(user)
        html_report = get_html_report(user.full_name, report_data)

        send_mail(
            email=user.email,
            email_content=html_report,
            subject=f"Monthly Quiz Report - {last_month.strftime('%B %Y')}"
        )

    print("Monthly reports sent successfully.")

@celery.task()
def export_users_csv(quiz_data):
   
    csv_path = "exported_users.csv"
    

    with open(csv_path, 'w', newline='') as csv_file:
        fieldnames = ['Name', 'Email', 'total_quizzes', 'average_score']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quiz_data)

    return csv_path

if __name__ == "__main__":
    with app.app_context():
        add_admin()
    app.run(debug=True, port=5001)
