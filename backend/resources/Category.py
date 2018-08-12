from flask import request
from flask_restful import Resource
from Model import db, Category, CategorySchema
from flask_jwt_extended import jwt_required

categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

class CategoryResource(Resource):

    def get(self):
        categories = Category.query.all()
        categories = categories_schema.dump(categories).data
        return {'status': 'success', 'data': categories}, 200

    @jwt_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # if type(json_data['name']) == str:
        #     data, errors = category_schema.load(json_data)
        # elif type(json_data['name']) == list:
        #     data, errors = categories_schema.load(json_data)
        # # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(name=data['name']).first()
        if category:
            return {'message': 'Category already exists'}, 400
        category = Category(
            name=json_data['name']
            )

        db.session.add(category)
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result },200

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id']).first()
        if not category:
            return {'message': 'Category does not exist'}, 400
        category.name = data['name']
        db.session.commit()

        result = category_schema.dump(category).data

        return { "status": 'success', 'data': result }, 202

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        var1 = 1
        category = Category.query.filter_by(id=data['id']).delete()
        db.session.commit()
        result = category_schema.dump(category).data

        return { "status": 'success', 'message': 'Category with id {} was deleted'.format(data['id'])},202

        # return { "status": 'success'}
