from flask import request
from flask_restful import Resource, Api
from models import db, User, Subject, Quiz, Chapter, Question
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from cache import cache


class QuestionApi(Resource):
    @cache.cached(timeout=10)
    @jwt_required()
    def get(self, question_id = None):
        if question_id:  
            question = Question.query.get(question_id)
            if question:
                return question.convert_to_json(), 200
            return {'message': 'Question does not exist.'}, 404

        search_query = request.args.get('search', '').strip()
        if search_query:
            questions = Question.query.filter(Question.question.ilike(f"%{search_query}%")).all()
        else:
            questions = Question.query.all() 
        
        print(questions)

        question_list = []

        for question in questions:
            question_list.append(question.convert_to_json())
        return question_list, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('question') and data.get('option1') and data.get('option2') and data.get('option3') and data.get('option4') and data.get('correct') and data.get('quiz_id')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 

            if len(data.get('question').strip()) > 300 or len(data.get('question').strip()) < 2:
                return {'message': 'Length of question should be in between 3 and 300'}, 400


            quiz = Quiz.query.get(data.get('quiz_id'))
            if not quiz:
                return {'message': 'Quiz not found'}
            
            que = Question.query.filter_by(question=data.get('question').strip()).first()

            if que:
                return {"message": "Question already exists."}, 409

            option1= data.get('option1') 
            option2= data.get('option2') 
            option3= data.get('option3') 
            option4= data.get('option4') 

            op = [option1,option2,option3,option4]

            new_question = Question(
                            question=data.get('question'), 
                            options='{}',
                            quiz_id=data.get('quiz_id'),
                            correct=data.get('correct')
                            )

            db.session.add(new_question)
            new_question.add_options(op)
            db.session.commit()
            return {'message': 'Question added successfully.'}, 201
        return {'message': 'Access Denied'}, 403



    @jwt_required()
    def put(self, question_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('question') and data.get('option1') and data.get('option2') and data.get('option3') and data.get('option4') and data.get('correct') and data.get('quiz_id')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 
            
        
            option1= data.get('option1') 
            option2= data.get('option2') 
            option3= data.get('option3') 
            option4= data.get('option4') 

            op = [option1,option2,option3,option4]

            question = Question.query.get(question_id)
            if question:
                question.question = data.get('question').strip()
                question.add_options(op)
                question.correct = data.get('correct')
                question.quiz_id = data.get('quiz_id')

                db.session.commit()
                return {'message': 'Question updated successfully.'}, 200 
            return {'message': 'Question does not exists.'}
        return {'message': 'Access Denied'}, 403

    @jwt_required()
    def delete(self, question_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            question = Question.query.get(question_id)
            if question:
                db.session.delete(question)
                db.session.commit()
                return {'message': 'Question Deleted successfully.'}, 200 
            return {'message': 'Question does not exists.'}
        return {'message': 'Access Denied'}, 403