from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema, RevokedTokenModel
from flask import current_app
from functools import wraps
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class LoginResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        user = User.authenticate(**data)

        if not user:
                return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(user.email)
        return {'message': 'Logged in as {}'.format(user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user = get_jwt_identity()
        # return a non-fresh token for the user
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
