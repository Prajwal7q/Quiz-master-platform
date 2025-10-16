from flask import request, jsonify 
from flask_restful import Resource
from models import db, User, Question, Score
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from flask_jwt_extended import jwt_required
from quiz_schedule import schedule_quizs
import json
from cache import cache

class UserDashboardApi(Resource):
    @cache.cached(timeout=10)    
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get("user_role") != "user":
            return {"message": "Invalid user"}, 401

        current_usr = current_user.get("user_id")

        student = User.query.filter_by(id=current_usr).first()

        quizs_data = schedule_quizs()

        history_quizs = [quiz.convert_to_json() for quiz in Score.query.filter_by(user_id=current_usr).all()]
        
        return {
            "student_name": student.full_name,
            "past_quizs": quizs_data["past"],
            "current_quizs": quizs_data["current"],
            "pre_quizs": quizs_data["pre"],
            "history_quizs": history_quizs,
        }, 200


###################################### exam api ###################################### 


class ExamApi(Resource):
    @cache.cached(timeout=10)
    @jwt_required()
    def get(self, id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'user':
            return {'message': "Invalid user"}, 401

        user_id = current_user.get('user_id')
        quiz_data = schedule_quizs()

        total_questions = Question.query.filter_by(quiz_id=id).count()

        if total_questions == 0:
            return {'message': "Exam will start soon"}, 200

        current_quiz_ids = [quiz['id'] for quiz in quiz_data['current']]
        if int(id) not in current_quiz_ids:
            return {'message': "Exam has not started yet or has already ended"}, 400

        # Pagination for questions
        question_no = request.args.get('page', 1, type=int)
        per_page = 1  # Fetch one question at a time
        questions = Question.query.filter_by(quiz_id=id).paginate(page=question_no, per_page=per_page)

        score = Score.query.filter_by(quiz_id=id, user_id=user_id).first()

        if score:
            answers = score.load_answers()
        else:
            answers = {}

        question_data = questions.items[0].convert_to_json()
        question_data.pop("correct", None)

        # Get the selected answer for the current question
        selected_answer = answers.get(str(questions.items[0].id), None)

        return {
            "quiz_id": id,
            "total_questions": total_questions,
            "current_page": question_no,
            "question": question_data,
            "answers": answers,
            "selected_answer": selected_answer  # Include the selected answer in the response
        }, 200

    @jwt_required()
    def post(self, id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'user':
            return {'message': "Invalid user"}, 401

        user_id = current_user.get('user_id')
        quiz_data = schedule_quizs()

        current_quiz_ids = [quiz['id'] for quiz in quiz_data['current']]
        if int(id) not in current_quiz_ids:
            return {'message': "Exam has not started yet or has already ended"}, 400

        data = request.json
        question_id = data.get('question_id')
        selected_option_index = data.get('selected_option')  # This is the index of the selected option
        submit_flag = data.get('submit')

        score = Score.query.filter_by(quiz_id=id, user_id=user_id).first()
        if not score:
            score = Score(user_id=user_id, quiz_id=id, start_time=datetime.now().time(), answers=json.dumps({}))
            db.session.add(score)
            db.session.commit()

        answers = json.loads(score.answers)
        print(f"Before update: {answers}")

        if question_id is not None and selected_option_index is not None:
            answers[str(question_id)] = selected_option_index
            score.answers = json.dumps(answers)
            db.session.commit()
            print(f"After update: {answers}")

        if submit_flag:
            correct_count = 0
            submitted_answers = json.loads(score.answers)
            total_questions = Question.query.filter_by(quiz_id=id).count()

            for qid, selected_index in submitted_answers.items():
                question = Question.query.filter_by(id=int(qid)).first()

                if question:
                    correct_index = question.correct   # This is an integer (index)
                    options = json.loads(question.options)  # Ensure options are loaded correctly

                    correct_index -= 1
                    print(f"Correct Index: {correct_index}, Options: {options}")
                    if 0 <= correct_index < len(options):
                        if int(selected_index) == correct_index:
                            correct_count += 1

            percentage = round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0

            print(f"Total Questions: {total_questions}, Correct Count: {correct_count}, Calculated Percentage: {percentage}")

            score.percentage = percentage
            score.end_time = datetime.now().time()
            db.session.commit()

            updated_score = Score.query.filter_by(quiz_id=id, user_id=user_id).first()
            print(f"Stored Percentage in DB: {updated_score.percentage}")

            return {"message": "Exam submitted successfully", "score": percentage}, 200

        return {"message": "Answer recorded successfully", "answers": answers}, 200






class ResultApi(Resource):
    @jwt_required()
    def get(self, score_id):
        current_user = json.loads(get_jwt_identity())

        if current_user.get("user_role") != "user":
            return {"message": "Invalid user"}, 401

        # Get past quizzes
        past_quizzes = schedule_quizs()["past"]
        past_quiz_ids = {quiz["id"] for quiz in past_quizzes}

        # Fetch score
        score = Score.query.filter_by(id=score_id).first()
        if not score:
            return {"message": "Score not found"}, 404

        # Check if the quiz is finished
        if score.quiz_id not in past_quiz_ids:
            return {"message": "Quiz is not finished yet"}, 400

        # Pagination and fetching questions
        per_page = 1
        question_no = request.args.get("page_p", 1, int)
        quiz_id = score.quiz_id

        # Fetch questions paginated
        questions = Question.query.filter_by(quiz_id=quiz_id).paginate(page=question_no, per_page=per_page)

        # Fetch user score
        user_id = current_user["user_id"]
        score_entry = Score.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
        question_id = questions.items[0].id if questions.items else None

        question_options = questions.items[0].load_options() if questions.items else []
        answers = score_entry.load_answers() if score_entry else {}
        chosen_answer_index = answers.get(str(question_id), None)

        response_data = {
            "quiz_id": quiz_id,
            "question_no": question_no,
            "total_questions": total_questions,
            "questions": [
                {
                    "id": q.id,
                    "question": q.question,
                    "options": q.load_options(),
                    "correct": q.correct -1,
                }
                for q in questions.items
            ],
            "answers": answers,
            "chosen_answer": chosen_answer_index,
        }

        return jsonify(response_data)
