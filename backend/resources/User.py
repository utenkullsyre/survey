from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema
from flask import current_app


users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):
    def get(self):
        # @token_required
        users = User.query.all()
        users = users_schema.dump(users).data
        return {'status': 'success', 'data': users}

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
        result = user_schema.dump(user).data
        #
        return { "status": 'success', 'data': result },202

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

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify
