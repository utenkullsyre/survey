from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema
from flask import current_app
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)


users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)

        if errors:
            return errors, 422
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User already exists'}, 400

        user = User(
            email=json_data['email'],
            password=json_data['password']
            )
        #
        db.session.add(user)
        db.session.commit()
        #
        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(user.email)
        #

        result = user_schema.dump(user).data
        #
        return { "status": 'success', 'user': result, 'tokens': {'access_token': access_token, 'refresh_token': refresh_token}},202

    @jwt_required
    def get(self):
        # @token_required
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(id=data['password']).first()
        if not category:
            return {'message': 'User does not exist'}, 400
        user.email = data['email']
        db.session.commit()

        result = user_schema.dump(user).data

        return { "status": 'success', 'data': result }, 202

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
            # if errors:
            #     return errors, 422
        var1 = 1
        category = User.query.filter_by(id=data['id']).delete()
        db.session.commit()
        result = user_schema.dump(category).data

        return { "status": 'success', 'message': 'User with id {} was deleted'.format(data['id'])},202

        # return { "status": 'success'}
