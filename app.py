import os
from datetime import datetime

from flask import Flask, request, make_response, Response
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

from werkzeug.contrib.atom import AtomFeed


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['REALLY_SIMPLE_RSS_SERVER_DB']

db = SQLAlchemy(app)

api = Api(app, default_mediatype='application/xml')


class Entry(db.Model):

    __tablename__ = 't_entry'
    id = db.Column(db.Integer, db.Sequence('entry_sequence'), primary_key=True)
    created_at_utc = db.Column(db.DateTime, default=datetime.utcnow)
    days_valid = db.Column(db.Integer)
    domain = db.Column(db.String, nullable=False)
    filter = db.Column(db.String)

    # RSS Atom Entry
    title = db.Column(db.String, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    content = db.Column(db.String)
    link = db.Column(db.String)



class Feed(Resource):

    def create_feed_from_db_entries(self, db_entries):
        """ See http://flask.pocoo.org/snippets/10/
        """
        feed_name = " - ".join([db_entries[0].domain, db_entries[0].filter])
        feed = AtomFeed(feed_name,
                        feed_url=request.url,
                        url=request.url_root)
        for entry in db_entries:
            feed.add(entry.title,
                     entry.content,
                     id=entry.id,
                     author='mymindwentblvnk',
                     url=entry.link,
                     updated=entry.updated,
                     published=entry.created_at_utc)
        return feed

    def post(self, domain, filter):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('link')
        parser.add_argument('category')
        parser.add_argument('summary')
        parser.add_argument('content')
        parser.add_argument('days_valid')
        args = parser.parse_args()

        title = args['title']
        link = args['link']
        category = args['category']
        summary = args['summary']
        content = args['content']
        days_valid = args['days_valid']

        entry = Entry(days_valid=days_valid,
                      domain=domain,
                      filter=filter,
                      title=title,
                      category=category,
                      summary=summary,
                      content=content,
                      link=link)
        db.session.add(entry)
        db.session.commit()

    def get(self, domain, filter):
        db_entries = Entry.query.\
                           filter_by(domain=domain).\
                           filter_by(filter=filter).\
                           all()
        feed = self.create_feed_from_db_entries(db_entries)
        xml = feed.get_response().get_data().decode('utf-8')
        return Response(xml, mimetype='text/xml')


api.add_resource(Feed, '/feed/<string:domain>/<string:filter>')


if __name__ == '__main__':
    app.run()
