from flask import Blueprint, current_app
from flask_restful import Api
from resources.Hello import Hello
from resources.Category import CategoryResource
from resources.Comment import CommentResource
from resources.User import UserResource
from resources.Login import LoginResource, TokenRefresh



api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

api.add_resource(Hello, '/Hello')
api.add_resource(CategoryResource, '/category')
api.add_resource(CommentResource, '/comment')
api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(TokenRefresh, '/refresh')
