from flask import request # current_app as app
from flask_restful import Resource, Api
from models import db, User, Subject, Quiz, Chapter
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from time_utils import time_converter,date_converter
import json
from cache import cache

class QuizApi(Resource):
    @cache.cached(timeout=10)
    @jwt_required()
    def get(self, quiz_id = None):
        if quiz_id:  
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                return quiz.convert_to_json(), 200

        search_query = request.args.get('search', '').strip()
        if search_query:
            quizes = Quiz.query.filter(Quiz.name.ilike(f"%{search_query}%")).all()
        else:
            quizes = Quiz.query.all()

        quiz_list = []

        for quiz in quizes:
            quiz_list.append(quiz.convert_to_json())
        return quiz_list, 200


    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json

            if not (data.get('name') and data.get('duration') and data.get('end_date') and data.get('end_time') and data.get('start_date') and data.get('start_time') and data.get('chapter_id')):
                return {'message': 'Bad request! All the data fields are required.'}, 400

            if len(data.get('name').strip()) > 120 or len(data.get('name').strip()) < 3:
                return {'message': 'Length of name should be between 3 and 120 characters.'}, 400

            chapter = Chapter.query.get(data.get('chapter_id'))
            if not chapter:
                return {'message': 'Chapter not found'}, 404
            
            quiz1 = Quiz.query.filter_by(name=data.get('name').strip()).first()

            if quiz1:
                return {"message": "Quiz already exists."}, 409


            start_time1 = time_converter(data.get('start_time')) if data.get('start_time') else None
            start_date1 = date_converter(data.get('start_date')) if data.get('start_date') else None
            end_date1 = date_converter(data.get('end_date')) if data.get('end_date') else None
            end_time1 = time_converter(data.get('end_time')) if data.get('end_time') else None


            if start_date1 and end_date1:
                if end_date1 < start_date1:
                    return {'message': 'Exam end date must be greater than or equal to the start date.'}, 400
                elif end_date1 == start_date1:
                    if end_time1 <= start_time1:
                        return {'message': 'Exam end time must be greater than or equal to the start time.'}, 400

            new_quiz = Quiz(
                name=data.get('name'),
                chapter_id=data.get('chapter_id'),
                duration=data.get('duration'),
                end_date=end_date1,
                end_time=end_time1,
                start_date=start_date1,
                start_time=start_time1
            )

            db.session.add(new_quiz)
            db.session.commit()

            return {'message': 'Quiz added successfully.'}, 201

        return {'message': 'Access Denied'}, 403

    @jwt_required()
    def put(self, quiz_id):
        current_user = json.loads(get_jwt_identity())

        if current_user.get('user_role') != 'admin':
            return {'message': 'Access Denied'}, 403

        data = request.json

        print(data)

        # Initialize variables for date and time conversions
        start_time1 = start_date1 = end_date1 = end_time1 = None

        if 'start_time' in data and data.get('start_time'):
            start_time1 = time_converter(data.get('start_time'))
        if 'start_date' in data and data.get('start_date'):
            start_date1 = date_converter(data.get('start_date'))
        if 'end_date' in data and data.get('end_date'):
            end_date1 = date_converter(data.get('end_date'))
        if 'end_time' in data and data.get('end_time'):
            end_time1 = time_converter(data.get('end_time'))
        
        # Fetch the quiz by ID
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return {'message': 'Quiz does not exist.'}, 404

        if start_date1 or end_date1:
            start_date_to_validate = start_date1 if start_date1 else quiz.start_date
            end_date_to_validate = end_date1 if end_date1 else quiz.end_date
            
            
            if end_date_to_validate < start_date_to_validate:
                return {'message': 'Exam end date must be greater than or equal to the start date.'}, 400
            elif end_date_to_validate == start_date_to_validate:
                start_time_to_validate = start_time1 if start_time1 else quiz.start_time
                end_time_to_validate = end_time1 if end_time1 else quiz.end_time
                
                if end_time_to_validate <= start_time_to_validate:
                    return {'message': 'Exam end time must be greater than or equal to the start time.'}, 400

        # Only update fields that exist in request data
        quiz.name = data.get('name') if data.get('name') else quiz.name
        quiz.chapter_id = data.get('chapter_id') if data.get('chapter_id') else quiz.chapter_id
        quiz.duration = data.get('duration') if data.get('duration') else quiz.duration
        quiz.start_date = start_date1 if start_date1 else quiz.start_date
        quiz.start_time = start_time1 if start_time1 else quiz.start_time
        quiz.end_date = end_date1 if end_date1 else quiz.end_date
        quiz.end_time = end_time1 if end_time1 else quiz.end_time

        try:

            db.session.commit()
            return {'message': 'Quiz updated successfully.'}, 200
        except Exception as e:

            db.session.rollback()
            return {'message': f'Error updating quiz: {str(e)}'}, 500

    @jwt_required()
    def delete(self, quiz_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                db.session.delete(quiz)
                db.session.commit()
                return {'message': 'Quiz Deleted successfully.'}, 200 
            return {'message': 'Quiz does not exists.'}, 404
        return {'message': 'Access Denied'}, 403