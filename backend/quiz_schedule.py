from models import Quiz
from datetime import datetime

def schedule_quizs():
    quizs = Quiz.query.all()
    now = datetime.now()  

    past, current, pre = [], [], []

    for i in quizs:
        start = datetime.combine(i.start_date, i.start_time)  
        end = datetime.combine(i.end_date, i.end_time)  

        if end < now:
            past.append(i.convert_to_json())  # Convert object to JSON before appending
        elif start > now:
            pre.append(i.convert_to_json())
        else:
            current.append(i.convert_to_json())

    return {"past": past, "current": current, "pre": pre}
