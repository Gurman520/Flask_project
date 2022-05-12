from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.tables import Article, User

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True, type=int)
parser.add_argument('text', required=True)


def abort_if_article_not_found(article_id):
    session = db_session.create_session()
    art = session.query(Article).get(article_id)
    if not art:
        abort(404, message=f"Article {article_id} not found")


class ArticleResource(Resource):
    def get(self, art_id):
        abort_if_article_not_found(art_id)
        session = db_session.create_session()
        arts = session.query(Article).get(art_id)
        return jsonify({'title': arts.title, 'author': arts.author, 'text': arts.text})


class ArticleListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        art = db_sess.query(Article)
        return jsonify(
            [{'id': item.id, 'title': item.title, 'author': item.author, 'status': item.status} for item in art])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        art = Article(
            title=args['title'],
            author=args['author'],
            text=args['text'],
            status=1
        )
        session.add(art)
        session.commit()
        return jsonify({'success': 'OK'})
