from flask import jsonify, make_response, request, g
from mailer import db
import datetime
from mailer.models.app import App
from mailer.util.validator import Validator
from mailer.util.user_token import UserToken
from mailer.util.api_key import ApiKey

class AppController:
    
    @staticmethod
    def regenerate_api_key(app_id, user_id):
        try:
            
            data = {
                'api_key':  ApiKey.generate_api_key(user_id, app_id),
                'created_at': datetime.datetime.utcnow()
            }
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            user_app.api_key = data.get('api_key', user_app.api_key)
            user_app.created_at = data.get('created_at', user_app.created_at)
            
            db.session.commit()
            
            return True
        
        except:
            
            return False
        
    
    @staticmethod
    def regenerate_key(app_id):
        
        try:
            
            user_id = g.user
            
            AppController.regenerate_api_key(app_id, user_id)
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            response = {
                "code": 200,
                "status": "success",
                "message": "Api Key Regenerated Successfully!",
                "app": user_app.to_dict()
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Regenerate Controller! {e}"
            }
            return jsonify(response), 500
        
    
    @staticmethod
    def get_all():
        
        try:
            
            user_id = g.user
            
            user_app = App.query.filter_by(user_id=user_id).all()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "User Apps Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "User Apps Found Successfully!"
            }
            response['app'] = [apps.to_dict() for apps in user_app]
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App GetAll Controller! {e}"
            }
            return jsonify(response), 500
        
    
    @staticmethod
    def get_app(app_id):
        
        try:
            
            user_id = g.user
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            if not user_app:
                response = {
                    "code": 404,
                    "status": "failure",
                    "message": "App Not Found!"
                }
                return jsonify(response), 404
            
            response = {
                "code": 200,
                "status": "success",
                "message": "App Found Successfully!"
            }
            response['app'] = user_app.to_dict()
            
            return jsonify(response), 200
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Get Controller! {e}"
            }
            return jsonify(response), 500
            
    
    @staticmethod
    def create_app(data):
        
        try:
            
            user_id = g.user
            
            if Validator.validate_name(data['app_name']) == False:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid Data!"
                }
                return jsonify(response), 400
            
            api_key = ''
            
            created_at = datetime.datetime.utcnow()
            
            new_app = App(
                user_id=user_id,
                app_name=data['app_name'],
                api_key=api_key,
                created_at=created_at
            )
            
            db.session.add(new_app)
            db.session.commit()
            
            app_id = new_app.app_id
            
            AppController.regenerate_api_key(app_id, user_id)
            
            user_app = App.query.filter_by(app_id=app_id).first()
            
            response = {
                "code": 201,
                "status": "success",
                "message": "App Created Successfully!",
                "app": user_app.to_dict()
            }
            
            return jsonify(response), 201
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Create Controller! {e}"
            }
            return jsonify(response), 500
    
    @staticmethod
    def delete_app(data):
    
        try:
            
            user_id = g.user
            
            if isinstance(data['app_id'], str):
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "Invalid AppID!"
                }
                return jsonify(response), 400
            
            user_app = App.query.filter_by(app_id=data['app_id']).first()
            
            if not user_app:
                response = {
                    "code": 400,
                    "status": "failure",
                    "message": "App does not Exists!"
                }
                return jsonify(response), 400
            
            db.session.delete(user_app)
            db.session.commit()
            
            response = make_response(
                    jsonify({
                    "code": 200,
                    "status": "success",
                    "message": "App Deleted Successfully!"
                }), 200
            )
            
            return response
        
        except Exception as e:
            response = {
                "code": 500,
                "status": "error",
                "message": f"Error App Delete Controller! {e}"
            }
            return jsonify(response), 500
        