from flask import request ,current_app
from flask_restful import Resource, Api
from models import db, Subject, Chapter
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
from cache import cache


class ChapterApi(Resource):
    @cache.cached(timeout=10)
    @jwt_required()
    def get(self, chapter_id = None):
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                return chapter.convert_to_json(), 200
            return {'message': 'Chapter does not exist.'}, 404

        search_query = request.args.get('search', '').strip()

        if search_query:
            chapters = Chapter.query.filter(Chapter.name.ilike(f"%{search_query}%")).all()
        else:
            chapters = Chapter.query.all()
        

        chapter_list = []

        for chapter in chapters:
            chapter_list.append(chapter.convert_to_json())
        return chapter_list, 200

    @jwt_required()
    def post(self):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('name') and data.get('about') and data.get('subject_id')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 

            if len(data.get('name').strip()) > 120 or len(data.get('name').strip()) < 3:
                return {'message': 'Length of name should be in between 3 and 60'}, 400

            if len(data.get('about').strip()) > 120 or len(data.get('about').strip()) < 1:
                return {'message': 'Length of about section should be in between 1 - 120'}

            subject = Subject.query.get(data.get('subject_id'))
            if not subject:
                return {'message': 'Subject not found'}
            
            chapter = Chapter.query.filter_by(name=data.get('name').strip(),subject_id=data.get('subject_id')).first()

            if chapter:
                return {"message": "Chapter already exists."}, 409

            new_chapter = Chapter(
                            name=data.get('name'), 
                            about=data.get('about'),
                            subject_id=data.get('subject_id')
                            )

            db.session.add(new_chapter)
            db.session.commit()
            return {'message': 'Chapter added successfully.'}, 201
        return {'message': 'Access Denied'}, 403



    @jwt_required()
    def put(self, chapter_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            data = request.json
            if not (data.get('name') and data.get('about')  and data.get('subject_id')):
                return {'message': ' Bad request! All the data fields are required.'}, 400 
            
            chapter1 = Chapter.query.filter_by(name=data.get('name').strip()).first()


        
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                chapter.name = data.get('name').strip() if data.get('name') else chapter.name
                chapter.about = data.get('about').strip() if data.get('about') else chapter.about
                chapter.subject_id = data.get('subject_id') if data.get('subject_id') else chapter.nasubject_idme
                db.session.commit()
                return {'message': 'Chapter updated successfully.'}, 200 
            return {'message': 'Chapter does not exists.'}, 404
        return {'message': 'Access Denied'}, 403

    @jwt_required()
    def delete(self, chapter_id):
        current_user = json.loads(get_jwt_identity())
        if current_user.get('user_role') == 'admin':
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                db.session.delete(chapter)
                db.session.commit()
                return {'message': 'Chapter Deleted successfully.'}, 200 
            return {'message': 'Chapter does not exists.'}, 404
        return {'message': 'Access Denied'}, 403