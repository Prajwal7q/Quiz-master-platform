from flask import Flask, Response
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from sqlalchemy import func
from models import db
from models import Score, User, Quiz
import numpy as np
from flask_login import current_user
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from sqlalchemy.sql import func, case

def data1():
    results = (
        db.session.query(
            Score,     
            
            func.count(Score.id).label('score_count'),
            func.max(Score.percentage).label('max'),
            func.avg(Score.percentage).label('avg'),
        )
        .group_by(Score.quiz_id)
        .all()
    )

    
    data = {row[0].quiz.name: row.score_count for row in results}
    avg = {row[0].quiz.name: [row.avg, row.max] for row in results}
    max = {row[0].quiz.name: row.max for row in results}
    print("Query Result as dict:", data,max,avg,results)
    return (data, avg)

def avg_score():
    avg1 = (
        db.session.query(
            func.avg(Score.percentage).label('avg'),
        )
        .all()
    )
    return  avg1[0][0]

def total_student():
    total = (
        db.session.query(
            func.count(User.id).label('user'),
        )
        .filter_by(is_admin =0)
        .all()
    )
    print(total)
    return  total[0][0]

def piechart():
    
    data = data1()[0]
    if not data:
        data = {"No quiz is attempted": 1}

    labels = list(data.keys())
    sizes = list(data.values())

    fig, ax = plt.subplots(figsize=(6, 6))

    def absolute_value(val):
        index = sizes.index(round(val / 100 * sum(sizes)))
        # print(f"{sizes[index]}")
        return f"{sizes[index]}"
    
    
    ax.pie(sizes, labels=labels, autopct=absolute_value, startangle=90)
    ax.axis('equal') 
    ax.set_title("Number of student attempt Quiz")

    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    plt.close(fig)

    return Response(img.getvalue(), mimetype='image/png')


def bar_chart():
    
    data = data1()[1]

    labels = list(data.keys())  
    avg_scores = [values[0] for values in data.values()]  
    max_scores = [values[1] for values in data.values()] 
    x = np.arange(len(labels)) 
    width = 0.35 

    fig, ax = plt.subplots(figsize=(8, 5))

    bars1 = ax.bar(x - width/2, avg_scores, width, label='Avg Score', color='skyblue')
    bars2 = ax.bar(x + width/2, max_scores, width, label='Max Score', color='orange')
    
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height()}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height()}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel("Quiz Name")
    ax.set_ylabel("Scores")
    ax.set_title("Comparison of Avg & Max Scores per Quiz")
    ax.set_xticks(x)
    ax.set_xticklabels(labels) 
    ax.legend()
    ax.set_ylim(0, 110)


    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    plt.close(fig)

    return Response(img.getvalue(), mimetype='image/png')


class AdminBarChartApi(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        user_id = current_user.get('user_id')
        user_role = current_user.get('user_role')

        if user_role == 'admin':
            return bar_chart()
        else:
            return {"message": "Access denied. Admins only."}, 403

class AdminPieChartApi(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        user_id = current_user.get('user_id')
        user_role = current_user.get('user_role')

        if user_role == 'admin':
            return piechart()
        else:
            return {"message": "Access denied. Admins only."}, 403



# Fetch user quiz data
def user_data(user_id):
    results = (
        db.session.query(
            Score.quiz_id,
            func.max(Score.percentage).label("max_score"),
            func.avg(Score.percentage).label("avg_score"),
            func.sum(case((Score.user_id == user_id, Score.percentage), else_=0)).label("current_user_score")
        )
        .group_by(Score.quiz_id)
        .all()
    )

    return results

# Generate the bar chart
def user_chart(user_id):
    data = user_data(user_id) 



    labels = [Quiz.query.filter_by(id=values[0]).first().name for values in data]
    avg_scores = [values[2] for values in data]
    max_scores = [values[1] for values in data]
    user_scores = [values[3] for values in data]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))

    bars1 = ax.bar(x - width, user_scores, width, label='Your Score', color='green')
    bars2 = ax.bar(x, avg_scores, width, label='Avg Score', color='skyblue')
    bars3 = ax.bar(x + width, max_scores, width, label='Max Score', color='orange')

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.1f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel("Quiz Name")
    ax.set_ylabel("Scores")
    ax.set_title("Comparison of Your Score, Avg Score & Max Score per Quiz")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0, ha='center')
    ax.legend()
    ax.set_ylim(0, 110)

    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close(fig)

    return Response(img.getvalue(), mimetype='image/png')

# RESTful API endpoint
class UserChartApi(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        user_id = current_user.get('user_id')
        user_role = current_user.get('user_role')

        if user_role == 'user':
            return user_chart(user_id)
        else:
            return {"message": "Access denied. Users only."}, 403
