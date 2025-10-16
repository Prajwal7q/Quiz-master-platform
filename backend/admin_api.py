from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, User, Subject, Score
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import func
from flask_jwt_extended import jwt_required
from flask_caching import Cache
import json

class AdminApi(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') != 'admin':
            return {"message": "Unauthorized access"}, 403
        
        total_students = self.total_student()

        # Get average score (rounded to 2 decimal places)
        avg_score_value = self.avg_score()
        avg_score_value = round(avg_score_value, 2) if avg_score_value else 0

        return {
            "total_students": total_students,
            "avg_score": avg_score_value
        }

    @staticmethod
    def total_student():
        total = (
            db.session.query(func.count(User.id))
            .filter_by(is_admin=0)
            .scalar()
        )
        return total or 0

    @staticmethod
    def avg_score():
        avg = (
            db.session.query(func.avg(Score.percentage))
            .scalar()
        )
        return avg or 0
