from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.tables import Article, User

parser = reqparse.RequestParser()
parser.add_argument('f_name', required=True)
parser.add_argument('s_name', required=True)
parser.add_argument('sex', required=True)
parser.add_argument('country', required=True)
parser.add_argument('email', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    art = session.query(User).get(user_id)
    if not art:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        use = session.query(User).get(user_id)
        return jsonify(
            {'name': use.name, 'surname': use.surname, 'email': use.email, 'country': use.country, 'sex': use.sex})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        use = session.query(User).get(user_id)
        if 'f_name' in request.json:
            use.name = request.json['f_name']
        if 's_name' in request.json:
            use.surname = request.json['s_name']
        if 'country' in request.json:
            use.country = request.json['country']
        if 'sex' in request.json:
            use.sex = request.json['sex']
        if 'email' in request.json:
            use.email = request.json['email']
        session.commit()
        return jsonify({'success': 'OK'})
