from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.tables import Article, Tag, User

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
        tag = list()
        for i in arts.tags:
            tag.append(i.name)
        return jsonify(
            {'title': arts.title, 'author': arts.author, 'author_name': session.query(User).get(arts.author).name,
             'text': arts.text, 'tags': tag, 'status': arts.status})

    def put(self, art_id):
        abort_if_article_not_found(art_id)
        session = db_session.create_session()
        art = session.query(Article).get(art_id)
        if 'title' in request.json:
            art.title = request.json['title']
        if 'text' in request.json:
            art.text = request.json['text']
        if 'status' in request.json:
            art.status = request.json['status']
        else:
            art.status = 1
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, art_id):
        abort_if_article_not_found(art_id)
        session = db_session.create_session()
        art = session.query(Article).get(art_id)
        session.delete(art)
        session.commit()
        return jsonify({'success': 'OK'})


class ArticleListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        art = db_sess.query(Article)
        return jsonify(
            [{'id': item.id, 'title': item.title, 'author': item.author,
              'author_name': db_sess.query(User).get(item.author).name,
              'text': item.text, 'status': item.status,
              'tags': [i.name for i in item.tags]} for item in art])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        art = Article(
            title=args['title'],
            author=args['author'],
            text=args['text'],
            status=1
        )
        for i in request.json['tegs']:
            tag = session.query(Tag).filter(Tag.name == i).first()
            art.tags.append(tag)
        session.add(art)
        session.commit()
        return jsonify({'success': 'OK'})


class TegResource(Resource):
    def post(self):
        session = db_session.create_session()
        teg = Tag(
            name=request.json['name']
        )
        session.add(teg)
        session.commit()
        return jsonify({'success': 'OK'})

    def get(self):
        db_sess = db_session.create_session()
        teg = db_sess.query(Tag)
        return jsonify({'tags': [i.name for i in teg]})
